from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser,BaseModel):
    username = models.CharField(unique=True,max_length=150,db_index=True)
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self):
        return self.username

    def is_member_of(self, community):
        return self.community_members.filter(community=community).exists()

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
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'

class AuthorFollow(BaseModel):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='followings')
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='followers')

    def __str__(self):
        return f"Author: {self.author.username} | Followed by: {self.user.username}"

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Foydalanuvchi o'ziga o'zi obuna bo'la olmaydi")

    class Meta:
        db_table = 'authorfollows'
        verbose_name = 'Obuna'
        verbose_name_plural = 'Obunalar'
        constraints = [
            models.UniqueConstraint(
                fields=['user','author'],
                name='unique_user_author_followings'
            ),
        ]
        indexes = [
            models.Index(fields=['user', 'author'],name='unique_user_author'),
            models.Index(fields=['author', 'user'],name='unique_author_user'),
        ]