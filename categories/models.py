from django.db import models
from core.models import BaseModel
from django.utils.text import slugify

class Category(BaseModel):
    name = models.CharField(max_length=100,db_index=True,unique=True)
    slug = models.SlugField(unique=True, db_index=True)

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
        db_table = "categories"
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Tag(BaseModel):
    name = models.CharField(max_length=100,db_index=True, unique=True)
    slug = models.SlugField(db_index=True,unique=True)

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
        db_table = "tags"
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"