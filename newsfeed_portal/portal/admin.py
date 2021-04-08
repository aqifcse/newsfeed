from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from jsonfield import JSONField
from django_json_widget.widgets import JSONEditorWidget
from portal.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "subscribe",
        "created_at",
        "updated_at",
    ]


class NewsCardAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "headline",
        "thumbnail",
        "source_of_news",
        "country_of_news",
        "original_news_source_link",
    ]


# ------------------RecommendWordList------------------
class WordListAdmin(admin.ModelAdmin):
    list_display = ("category", "word", "created")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("recommended_by", "name")


admin.site.register(WordList, WordListAdmin)
admin.site.register(Category, CategoryAdmin)

# ---------------------------------------------------

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(NewsCard, NewsCardAdmin)
