# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from django.utils import timezone as tz
from jsonfield import JSONField


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



# To Do for settings
class Category(models.Model): # The Category table name that inherits models.Model
	name = models.CharField(max_length=100) #Like a varchar

	class Meta:
		verbose_name = ("Category")
		verbose_name_plural = ("Categories")

	def __str__(self):
		return self.name #name to be shown when called

class TodoList(models.Model): #Todolist able name that inherits models.Model
	title = models.CharField(max_length=250) # a varchar
	content = models.TextField(blank=True) # a text field 
	created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
	due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date
	category = models.ForeignKey(Category, default="general", on_delete=models.CASCADE) # a foreignkey

	class Meta:
		ordering = ["-created"] #ordering by the created field

	def __str__(self):
		return self.title #name to be shown when called

