from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class CustomUser(AbstractUser):
   user_type_data = ((1, "Admin"), (2, "User"))
   user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
   id = models.AutoField(primary_key=True)
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   objects = models.Manager()


class User(models.Model):
   phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
   id = models.AutoField(primary_key=True)
   admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
   mobile = models.CharField(validators=[phone_regex], max_length=17, blank=True)
   address = models.TextField()
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now_add=True)
   objects = models.Manager()



class FileData(models.Model):
   username = models.CharField(max_length=50)
   key = models.CharField(max_length=50)
   file_title = models.CharField(max_length=50)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   objects = models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            User.objects.create(admin=instance, address="")


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.user.save()