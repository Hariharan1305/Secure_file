from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .EmailBackEnd import EmailBackEnd
from .models import CustomUser
from django.core.files.storage import FileSystemStorage
import pyAesCrypt
import os
from . import models
import pandas as pd

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def logout(request):
    return HttpResponseRedirect("/")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, email=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request,)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect("/user_home")
            else:
                return HttpResponseRedirect("/login")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/login")



#admin:
def admin_home(request):
    return render(request, "admin_home.html")





#user:
def user_home(request):
    return render(request, "user_home.html")

def add_user_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password, user_type=2)
            user.user.mobile=mobile
            user.user.address=address
            user.save()
            messages.success(request, "Successful")
            return HttpResponseRedirect("/login")

        except:
            messages.error(request, "Failed")
            return HttpResponseRedirect("/signup")

def upload(request):
    if 'upload' in request.POST:
        key = request.POST['key']
        file = request.FILES['file']

        fs = FileSystemStorage("securefile_app/media/")
        fs1 = FileSystemStorage("securefile_app/enc/")

        f_data = fs.save(file.name,file)
        location = os.getcwd()
        bufferSize = 1024 * 1024
        pyAesCrypt.encryptFile(location + "\\" + fs.base_location + file.name,
                               location + "\\" + fs1.base_location + file.name + ".aes", key, bufferSize)
        print(fs1.base_location)
        #file1 = fs1.open( file.name + ".aes")

        k = models.FileData.objects.create(file_title=file.name + ".aes", key=key)
        k.save()

    return render(request, 'upload.html')


def file_view(request):
    fs = FileSystemStorage("securefile_app\\media\\")
    fs1 = FileSystemStorage("securefile_app\\enc\\")
    fs2 = FileSystemStorage("securefile_app\\dec\\")
    location  = os.getcwd()
    print(os.listdir(location+"/"+fs.base_location))

    # encryption/decryption buffer size - 64K
    bufferSize = 1024 * 1024
    if request.method=="POST":
        id = request.POST["download"]
        password =request.POST["key"]
        j = models.FileData.objects.get(id=id)
        print("enc happend")
        file1 = fs1.open(j.file_title)
        print(location+"\\"+fs2.base_location+j.file_title+".aes")
    # encrypt
        #pyAesCrypt.encryptFile(location+"\\"+fs.base_location+j.file_title, location+"\\"+fs1.base_location+j.file_title+".aes", password, bufferSize)
    # decrypt
        try:
            pyAesCrypt.decryptFile(fs1.base_location+j.file_title,fs2.base_location+j.file_title, password, bufferSize)
            file1 = fs2.open(j.file_title)
            response = HttpResponse(file1, content_type='application')
            return response
        except Exception as e:
            return HttpResponse(e)
        #response = HttpResponse(file2, content_type='application')
        #return response
    #return render(request,"fileview.html",{"files":os.listdirlocation+"/"+fs.base_location})
    j = models.FileData.objects.all()
    return render(request,"fileview.html",{"files":j})

def output(request): #not used
    j = models.FileData.objects.all()
    l = []
    for jk in j:
        l.append(jk)
    # mm = open(settings.MEDIA_ROOT)
    print(len(l))
    fs = FileSystemStorage()
    mm = fs.open(l[len(l)-1].file_title)
    print(mm)
    df = pd.read_csv(mm)
    #print(df.values.tolist())
    i = df.plot().get_figure()
    i.savefig('media//a.png')
    fs = FileSystemStorage()

    return HttpResponse(fs.open('a.png').file,content_type='image/png')
    #response = HttpResponse(file,content_type='application')
    #return response
    #return  HttpResponse("<a href = 'input/'>output</a>")