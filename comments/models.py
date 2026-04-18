from django.db import models
from core.models import BaseModel
from articles.models import Article
from django.conf import settings

class Comment(BaseModel):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments',db_index=True)
    content = models.TextField(max_length=500)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,related_name='replies',null=True,blank=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
      return self.content[:30]

    @property
    def is_parent(self):
       return self.parent is None

    class Meta:
      db_table = 'comments'
      verbose_name = 'Kommentariy'
      verbose_name_plural = 'Kommentariylar'

class Like(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='article_likes')

    def __str__(self):
       return f"Liked by: {self.user.username} | article: {self.article.title}"

    class Meta:
       db_table = 'likes'
       verbose_name = 'Like'
       verbose_name_plural = 'Likelar'
       constraints = [models.UniqueConstraint(
             fields=['user','article'],
             name='uniq_user_article_like',
       )]