from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from portal.views import *
from portal.forms import EmailValidationOnForgotPassword
from django.conf.urls.static import static
from django.conf import settings

# REST
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path(
        "userReadListTrack",
        UserReadListTrackAPIView.as_view(),
        name="userReadListTrack",
    ),
    path(
        "subscribeUpdate",
        SubscribeUpdateAPIView.as_view(),
        name="subscribeUpdate",
    ),
    path(
        "newsLetterUpdate",
        NewsLetterUpdateAPIView.as_view(),
        name="newsLetterUpdate",
    ),
    path(
        "readListDelete",
        ReadListDeleteAPIView.as_view(),
        name="readListDelete",
    ),
    # NewsLetterAPIView
    path("admin/", admin.site.urls),
    path("", include("portal.urls", namespace="portal")),
    path(
        "login/", UserLoginView.as_view(template_name="users/login.html"), name="login"
    ),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path(
        "password-reset/",
        MyPasswordRestView.as_view(form_class=EmailValidationOnForgotPassword),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", global_home, name="global_home"),
    path("next", loadcontent, name="Loadcontent"),
    path("routers/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
