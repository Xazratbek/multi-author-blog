from celery import shared_task
from .models import Notification
from articles.models import Article
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser, AuthorFollow

@shared_task
def send_new_post_notifications(slug):
    article = get_object_or_404(Article,slug=slug)
    followers = CustomUser.objects.filter(
        id__in=AuthorFollow.objects.filter(
            author=article.author
        ).values_list("user_id", flat=True)
    )

    print(article.author)
    print(list(followers))

    notifications = [
        Notification(
            user=user,
            type="new_post",
            message=f"{article.author.username} yangi maqola chiqardi: {article.title}",
            content_type='article',
            object_id=article.id
        )
        for user in followers
    ]

    Notification.objects.bulk_create(notifications)