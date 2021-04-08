from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.utils import timezone as tz
from jsonfield import JSONField


class User(AbstractUser):
    subscribe = models.BooleanField(
        default=False,
        help_text="This will enlist you to newsletter feature. You will get emails on latest news updates. To stop getting emails please set this field false",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewsCard(models.Model):
    headline = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.URLField()
    source_of_news = models.CharField(max_length=100, null=True, blank=True)
    country_of_news = models.CharField(max_length=100, null=True, blank=True)
    original_news_source_link = models.URLField()

    published_at = models.DateTimeField(default=tz.now)


class Category(models.Model):
    # recommended_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class WordList(models.Model):
    category = models.ForeignKey(Category, default="general", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)

    content = models.TextField(blank=True)
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title
