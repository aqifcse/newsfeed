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
    path("admin/", admin.site.urls),
    path("", include("portal.urls", namespace="portal")),
    path(
        "login/", UserLoginView.as_view(template_name="users/login.html"), name="login"
    ),
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
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
    # path('', GlobalHomeView.as_view(), name='global_home'),
    path("", global_home, name="global_home"),
    path("next", loadcontent, name="Loadcontent"),
    path(
        "global-country-based-news/",
        GlobalCountryBasedNewsView.as_view(),
        name="global_country_based_news",
    ),
    path(
        "global-source-based-news/",
        GlobalSourceBasedNewsView.as_view(),
        name="global_source_based_news",
    ),
    path(
        "global-keyword-based-news/",
        GlobalKeywordBasedNewsView.as_view(),
        name="global_keyword_based_news",
    ),
    path("routers/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
