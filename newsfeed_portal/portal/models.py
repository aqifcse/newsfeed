from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils import timezone as tz


class User(AbstractUser):
    subscribe = models.BooleanField(
        default=False,
        help_text="This will enlist you to newsletter feature. You will get newsletter emails on latest news updates(within every 15 minutes). To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ReadList(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    country = models.CharField(
        max_length=50, null=True, blank=True
    )  # ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    source = models.CharField(
        max_length=50, null=True, blank=True
    )  # ForeignKey(Source, on_delete=models.SET_NULL, null=True)

    top_headlines_url = models.URLField()
    full_stories_url = models.URLField()

    newsletter = models.BooleanField(
        default=False,
        help_text="Checking this box will send you newsletters to your email id about the latest news updates(within every 15 minutes) based on this readlist. To stop getting news please set this field unchecked",
    )
    created_at = models.DateTimeField(default=tz.now)

    slug = models.SlugField(max_length=40)

    def __str__(self):
        return str(self.keyword)

    def slug(self):
        return slugify(self.keyword)

    class Meta:
        verbose_name = "ReadList"
        verbose_name_plural = "ReadLists"


class ReadListNewsBody(models.Model):
    readlist = models.ForeignKey(ReadList, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200, unique=True)
    thumbnail = models.URLField()
    source_of_news = models.CharField(max_length=100, null=True, blank=True)
    country_of_news = models.CharField(max_length=100, null=True, blank=True)
    original_news_source_link = models.URLField()
    published_at = models.DateTimeField(default=tz.now)

    slug = models.SlugField(max_length=40)

    def __str__(self):
        return str(self.headline)

    def slug(self):
        return slugify(self.headline)

    class Meta:
        verbose_name = "ReadListNewsBody"
        verbose_name_plural = "ReadListNewsBodies"
