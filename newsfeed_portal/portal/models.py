from django.db import models
from jsonfield import JSONField
from django.utils import timezone as tz

class News(models.Model):
    headline = models.CharField(max_length=200, null=True, blank=True)
    #thumbnail =
    source_country = models.CharField(max_length=100, null=True, blank=True)
    source_name  = models.CharField(max_length=100, null=True, blank=True)
    source_link = models.URLField() 
    created_at = models.DateTimeField(default=tz.now)