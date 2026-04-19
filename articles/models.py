from django.db import models
from core.models import BaseModel
from django.conf import settings
from django.utils.text import slugify
from categories.models import Category, Tag

class ArticleStatusChoice(models.TextChoices):
    DRAFT = 'draft', 'Qoralama'
    TEKSHIRUVDA = 'in_progress', 'Tekshiruvda'
    PUBLISHED = 'published', 'Chop etilgan'
    REJECTED = 'rejected', 'Bekor qilingan'
    ARXIV = 'arxiv', 'Arxivlangan'

class Article(BaseModel):
    title = models.CharField(max_length=150,db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='articles')
    status = models.CharField(max_length=40,choices=ArticleStatusChoice.choices, default=ArticleStatusChoice.DRAFT,db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(Tag, related_name='posts')
    published_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug

            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'articles'
        verbose_name = 'Maqola'
        verbose_name_plural = 'Maqolalar'

class ArticleView(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='views')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        view_count = self.__class__.objects.filter(article=self.article).count()
        return f"Article: {self.article.title} | Views: {view_count}"

    class Meta:
        db_table = 'article_views'
        verbose_name = 'Maqola ko\'rishlari'
        verbose_name_plural = 'Maqola ko\'rishlari'

        constraints = [
            models.UniqueConstraint(fields=['article', 'session_key'], name='unique_session_view'),
            models.UniqueConstraint(fields=['article', 'user'], name='unique_user_view'),
        ]
