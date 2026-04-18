from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Article, Comment, Like

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent')

        if not content:
            return JsonResponse({"status": 400, "message": "Kommentariya matni bo'sh bo'lishi mumkin emas"}, status=400)

        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)

        comment = Comment.objects.create(article=article,user=request.user,content=content,parent=parent_comment
        )

        return JsonResponse({
            "status": 201,
            "message": "Comment qoldirildi",
            "comment_id": comment.id,
            "username": request.user.username,
            "content": comment.content,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at.strftime("%d %b %Y %H:%M"),
        }, status=201)

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        comment_slug = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_slug)

        return comment.user == self.request.user

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return JsonResponse({"status": 200,'message': "Comment o'chirildi", "comment_id": comment_id})

class LikeToggleView(LoginRequiredMixin,View):
    def post(self, request,slug):
        article = get_object_or_404(Article,slug=slug)
        like, created = Like.objects.get_or_create(user=request.user,article=article)
        if not created:
            like.delete()
            return JsonResponse({"status": 200,'message': 'Like o\'chirildi', 'liked': False, 'count': article.article_likes.count()})

        return JsonResponse({"status": 201,'message':'Liked', 'liked': True, 'count': article.article_likes.count()})
