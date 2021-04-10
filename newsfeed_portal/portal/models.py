from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils import timezone as tz


class User(AbstractUser):
    subscribe = models.BooleanField(
        default=False,
        help_text="This will enlist you to newsletter feature. You will get newsletter emails on latest news updates(within every 15 minutes). To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class NewsReader(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.headline)


class NewsBody(models.Model):
    news = models.ForeignKey(NewsReader, on_delete=models.CASCADE)
    thumbnail = models.URLField()
    source_of_news = models.CharField(max_length=100, null=True, blank=True)
    country_of_news = models.CharField(max_length=100, null=True, blank=True)
    original_news_source_link = models.URLField()

    published_at = models.DateTimeField(default=tz.now)


class ReadList(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)

    newsletter = models.BooleanField(
        default=False,
        help_text="Checking this box will send you newsletters to your email id about the latest news updates(within every 15 minutes) based on this readlist. To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(default=tz.now)