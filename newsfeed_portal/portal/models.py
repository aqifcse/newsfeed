from django.db import models
from jsonfield import JSONField
from django.utils import timezone as tz
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    subscribe = models.BooleanField(
        default=False, 
        help_text="This will enlist you to newsletter feature. You will get emails on latest news updates. To stop getting emails please set this field false"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecommendTags(models.Model):
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE)
    country_tags        = JSONField(max_length=1000)
    news_source_tags    = JSONField(max_length=1000)
    keywords_tags       = JSONField(max_length=1000)
    

class NewsCard(models.Model):
    headline                    = models.CharField(max_length=200, null=True, blank=True)
    thumbnail                   = models.URLField()
    source_of_news              = models.CharField(max_length=100, null=True, blank=True)
    country_of_news             = models.CharField(max_length=100, null=True, blank=True)
    original_news_source_link   = models.URLField()

    published_at                = models.DateTimeField(default=tz.now)