from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from articles.models import Article

class NotificationListView(LoginRequiredMixin,View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user,is_read=False).order_by('-created_at')
        if not notifications.exists():
            return JsonResponse({"status": 200,'message': 'Bildirishnomalar mavjud emas', 'data': [], 'count': 0})

        data = []
        for notification in notifications:
            url = '#'
            if notification.content_type == 'article' and notification.object_id:
                article = Article.objects.filter(id=notification.object_id).only('slug').first()
                if article:
                    url = f"/articles/{article.slug}/"
            data.append(
                {
                    "id": notification.id,
                    'type': notification.type,
                    'message': notification.message,
                    'content_type': notification.content_type,
                    'object_id': notification.object_id,
                    'created_at': notification.created_at.strftime("%d %b %Y %H:%M"),
                    'url': url,
                }
            )

        return JsonResponse({"status": 200,'message':'O\'qilmagan bildirishnomalar','data': data, 'count': len(data)})


class NotificationReadView(LoginRequiredMixin, View):
    def get(self, request,id):
        notification = Notification.objects.filter(id=id,user=request.user,is_read=False).first()
        if notification:
            notification.is_read = True
            notification.save()
            return JsonResponse({"status": 200,'message': "Bildirishnoma o'qilgan deb belgilandi"})
        else:
            return JsonResponse({"status": 204,'message': 'Bildirishnoma topilmadi'})

class MarkAsReadAllNotifications(LoginRequiredMixin, View):
    def post(self,request):
        try:
            request.user.notifications.filter(is_read=False).update(is_read=True)
            return JsonResponse({"status": 200,'message': 'Barcha bildirishnomalar o\'qilgan deb belgilandi'})

        except Exception as e:
            return JsonResponse({"status": 400, 'message': str(e)})
