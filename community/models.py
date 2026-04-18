from django.db import models
from core.models import BaseModel
from django.conf import settings
from django.utils.text import slugify

class CommunityRoleChoice(models.TextChoices):
    OWNER = 'owner', "Ega"
    MEMBER = 'member', "Hamjamiyat a'zosi"

class Community(BaseModel):
    name = models.CharField(max_length=150,unique=True, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='communities',db_index=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'communities'
        verbose_name = 'Hamjamiyat'
        verbose_name_plural = 'Hamjamiyatlar'

class CommunityMembership(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='community_members',db_index=True)
    community = models.ForeignKey(Community,on_delete=models.CASCADE,related_name='members',db_index=True)
    role = models.CharField(max_length=15,db_index=True,choices=CommunityRoleChoice.choices,default=CommunityRoleChoice.MEMBER)

    def __str__(self):
        return f"{self.user.username} is {self.role} of {self.community.name}"

    class Meta:
        db_table = 'community_members'
        verbose_name = 'Hamjamiyat a\'zosi'
        verbose_name_plural = 'Hamjamiyat a\'zolari'
        constraints = [
            models.UniqueConstraint(
                fields=['user','community'],
                name='unique_user_community'
            )
        ]


class CommunityMessage(BaseModel):
    community = models.ForeignKey(Community,on_delete=models.CASCADE,related_name='messages',db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='author_messages',db_index=True)
    content = models.TextField(max_length=150)

    def __str__(self):
        return f"Message from: {self.author.username} | in community: {self.community.name}"

    class Meta:
        db_table = 'community_messages'
        verbose_name = 'Hamjamiyat xabari'
        verbose_name_plural = 'Hamjamiyat xabarlari'