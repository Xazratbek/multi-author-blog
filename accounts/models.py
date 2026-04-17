from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel

class CustomUser(AbstractUser,BaseModel):
    username = models.CharField(max_length=150,db_index=True)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

class Profile(BaseModel):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField()
    age = models.PositiveIntegerField(null=True,blank=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True,default='users/default_user.jpg')
    telegram_url = models.URLField(null=True, blank=True)
    linked_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'