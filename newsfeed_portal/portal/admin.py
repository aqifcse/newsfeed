from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from jsonfield import JSONField
from django_json_widget.widgets import JSONEditorWidget
from portal.models import *

admin.site.unregister(Group)


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "subscribe",
    ]


admin.site.register(User, UserAdmin)


class ReadListNewsBodyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "readlist",
        "headline",
        "thumbnail",
        "source_of_news",
        "country_of_news",
        "original_news_source_link",
    ]


admin.site.register(ReadListNewsBody, ReadListNewsBodyAdmin)


class ReadListAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "keyword", "source", "country", "newsletter")


admin.site.register(ReadList, ReadListAdmin)