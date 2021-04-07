from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from jsonfield import JSONField
from django_json_widget.widgets import JSONEditorWidget
from portal.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'subscribe', 
        'created_at', 
        'updated_at'
    ]

class RecommendTagsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'country_tags', 
        'news_source_tags',
        'keywords_tags', 
    ]

    formfield_overrides = {
        # fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        models.JSONField: {
            'widget': JSONEditorWidget
        },
    }

class NewsCardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'headline',
        'thumbnail',
        'source_of_news',
        'country_of_news',
        'original_news_source_link',   
    ]
#------------------To do------------------
class TodoListAdmin(admin.ModelAdmin):
	list_display = ("title", "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name",)

admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Category, CategoryAdmin)

#---------------------------------------------------

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(RecommendTags, RecommendTagsAdmin)
admin.site.register(NewsCard, NewsCardAdmin)



