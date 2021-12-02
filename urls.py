from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('doLogin', views.doLogin, name="doLogin"),


    #admin:
    path('admin_home', views.admin_home, name="admin_home"),


    #user:
    path("user_home", views.user_home, name="user_home"),
    path("add_user_save", views.add_user_save, name="add_user_save"),
    path("upload", views.upload, name="upload"),
    path('view', views.file_view,name="view"),
]