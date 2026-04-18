from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Notification
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class NotificationListView(LoginRequiredMixin,View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user,is_read=False)
        if not notifications.exists():
            return JsonResponse({"status": 204,'message': 'Bildirishnomalar mavjud emas'})

        data = []
        for notification in notifications:
            data.append(
                {
                    "id": notification.id,
                    'type': notification.type,
                    'message': notification.message,
                    'content_type': notification.content_type,
                    'object_id': notification.object_id,
                }
            )

        return JsonResponse({"status": 200,'message':'O\'qilmagan bildirishnomalar','data': data})


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
    def get(self,request):
        try:
            request.user.notifications.bulk_update(is_read=True)
            return JsonResponse({"status": 200,'message': 'Barcha bildirishnomalar o\'qilgan deb belgilandi'})

        except Exception as e:
            return JsonResponse({"status": 400, 'message': e})