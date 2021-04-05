from django.contrib import admin
from .models import AppDeveloper, User, AppUser, App, AppAuthor


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active')
    search_fields = ['username']
    list_filter = ['username']


admin.site.register(User, UserModelAdmin)
admin.site.register(AppDeveloper)
admin.site.register(AppUser)
admin.site.register(App)
admin.site.register(AppAuthor)
