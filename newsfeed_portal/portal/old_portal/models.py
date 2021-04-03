from django.db import models
from django.template.defaultfilters import slugify

from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

from django.core.validators import FileExtensionValidator
from django.contrib.contenttypes.fields import GenericRelation
from django_cleanup.signals import cleanup_post_delete
from sorl.thumbnail import delete

from django.db.models import Func

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class User(AbstractUser):
    is_developer = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)


class AppDeveloper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=70, blank=True)
    is_active = models.BooleanField(default=False)


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=70, blank=True)
    is_active = models.BooleanField(default=False)

class AppAuthor(models.Model):
    author = models.ForeignKey(AppDeveloper, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=200, unique=True) 

    def __str__(self):
        return str(self.app_name)

class App(models.Model):
    app_file = models.FileField(
        upload_to='apk/', 
        default=None, 
        blank = False,
        help_text="Allowed file extension .apk",
        validators=[FileExtensionValidator(allowed_extensions=['apk'])]
    )

    app_logo = models.ImageField( 
        upload_to='logo/', 
        null=True, 
        blank=True, 
        editable=True, 
        help_text="Image size has to be in JPG/PNG", 
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg'])]
    )
    app = models.ForeignKey(AppAuthor, on_delete=models.CASCADE)
    app_version_code = models.PositiveIntegerField()
    app_version_name = models.CharField(max_length=200)
    app_package_name = models.CharField(max_length=200, null=True, 
        blank=True)
    app_short_description = models.CharField(max_length=200, null=True, 
        blank=True)
    app_long_description = models.TextField(
        null=True, blank=True)
    app_release_note = models.CharField(max_length=200)
    app_update_notice = models.CharField(
        max_length=200, 
        default = "An updated version of this App is available. Please install the updated version of this App."
    )
    

    downloads = models.IntegerField(default=0)

    slug = models.SlugField(max_length=40)

    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.app.app_name)

    def slug(self):
        return slugify(self.app.id)

    def total_upload(self):
        return App.objects.all().count()

    class Meta:
        verbose_name = 'App'
        verbose_name_plural = 'Apps'

