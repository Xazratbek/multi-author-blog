from django.db import models
from core.models import BaseModel
from django.conf import settings

class NotificationTypeChoice(models.TextChoices):
    NEW_POST = 'new_post', 'Yangi post'
    COMMUNITY_MESSAGE = 'community_messages', 'Hamjamiyatdan xabar'

class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications',db_index=True)
    type = models.CharField(max_length=35,choices=NotificationTypeChoice.choices)
    message = models.TextField(max_length=300)
    is_read = models.BooleanField(default=False,db_index=True)
    content_type = models.CharField(max_length=150,db_index=True,null=True,blank=True)
    object_id = models.PositiveBigIntegerField(null=True,blank=True)

    def __str__(self):
        return f"Notification to: {self.user.username} | Type: {self.type} | Message: {self.message[:30]}"

    def send_notification(self,user,type,message,content_type,object_id):
        try:
            notification = self.__class__.objects.create(user=user,type=type,message=message,content_type=content_type,object_id=object_id)
            return notification

        except Exception as e:
            return e

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'