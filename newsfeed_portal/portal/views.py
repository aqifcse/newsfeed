import datetime

from .forms import *
from .models import *
from .tokens import account_activation_token

# from .serializers import UserUpdateSerializer

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import *
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.db import transaction
from django.db.models import Q
from django.db.models import Count, Value, F, Sum
from django.db.models.functions import Concat

from django.http import FileResponse, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect

from django.template import RequestContext
from django.template.loader import render_to_string

from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy, reverse

from django.views.generic import *
from django.views.generic.detail import *

# ------------------------------------------REST-framework-----------------------------------------
from rest_framework import viewsets, permissions, filters
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# ------------------------------------------NewsAPI Packages-------------------------------------------------
from newsapi.newsapi_client import NewsApiClient


# -------------------------------------------View Func and Class starts------------------------------------
class UserLoginView(LoginView):
    form_class = UserAuthForm

    def get_success_url(self):
        if self.request.user:
            return reverse("portal:user_home")
        else:
            return reverse("portal:user_home")

    def form_invalid(self, form):
        # error message
        error_messages = []
        message = form.errors.get_json_data()
        for _, message_value in message.items():
            error = message_value[0]["message"]
            error_messages.append(error)
        message_ = " And ".join(error_messages)

        # Check user_type
        user_type = "asdfa"
        if user_type:
            messages.error(self.request, message_)
            return redirect("login")
        elif user_type:
            messages.error(self.request, message_)
            return redirect("login")
        return self.render_to_response(self.get_context_data(form=form))

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = "users/signup_form.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user_type": "User",
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = "Activate Your User account in NewsFeed Portal"
            message = render_to_string(
                "users/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(
                subject, message, "<your aws smtp sending mail id e.g. x@y.com>"
            )

            email_sent_message = (
                "An email has been sent to "
                + str(user.email)
                + " Please check your email and click on the confirmation link to confirm your account"
            )

            return render(
                request,
                "users/login.html",
                {
                    "success_message": email_sent_message,
                },
            )

        return render(request, self.template_name, {"form": form})


class MyPasswordRestView(PasswordResetView):
    from_email = "<your aws smtp mail id e.g x@y.com>"
    html_email_template_name = "users/password_reset_email_template.html"
    subject_template_name = "users/password_reset_subject.txt"
    template_name = "users/password_reset.html"


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            print(uid)
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            print("Does not exists")
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user:
                user.is_active = True

            user.email_confirmed = True
            user.save()
            login(request, user)

            if user:
                user_success_account_message = email_sent_message = (
                    "Hi!! "
                    + str(user.username)
                    + " Your account have been confirmed. Please log with your given username and password."
                )

                return render(
                    request,
                    "users/login.html",
                    {
                        "success_message": user_success_account_message,
                    },
                )
        else:
            return render(
                request,
                "users/login.html",
                {
                    "error_message": "The confirmation link was invalid, possibly because it has already been used."
                },
            )


class GlobalHomeView(ListView):
    model = NewsBody
    template_name = "portal/global_home.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


class GlobalCountryBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/global_country_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


class GlobalSourceBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/global_source_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


class GlobalKeywordBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/global_keword_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name="dispatch")
class UserHomeView(ListView):
    model = NewsBody
    template_name = "portal/user_home.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name="dispatch")
class UserCountryBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/user_country_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name="dispatch")
class UserSourceBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/user_source_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name="dispatch")
class UserKeywordBasedNewsView(ListView):
    model = NewsBody
    template_name = "portal/user_keyword_based_news.html"
    context_object_name = "feeds"
    paginate_by = 15

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return NewsBody.objects.filter(
                Q(image_url__icontains=form)
                | Q(result__icontains=form)
                | Q(created_at__icontains=form)
            )
        queryset = NewsBody.objects.all().order_by("published_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@login_required
def user_profile_settings(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return render(
                request,
                "portal/user_profile_settings.html",
                {"u_form": u_form, "message": "Your account has been updated!"},
            )
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        "u_form": u_form,
    }
    return render(request, "portal/user_profile_settings.html", context)


@login_required
def user_news_recommend_settings(request):
    words = WordList.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":

        username = request.user.username
        user_obj = get_object_or_404(User, username=username)

        if "taskAdd" in request.POST:
            word = request.POST.get("description", False)
            category = request.POST.get("category_select", False)

            if category != "":
                word_object = WordList(
                    word=word,
                    category=Category.objects.get(
                        recommended_by=user_obj, name=category
                    ),
                )
                word_object.save()
                return redirect("portal:user_news_recommend_settings")
            else:
                return redirect("portal:user_news_recommend_settings")

        if "taskDelete" in request.POST:
            checked_word_id = request.POST.get("checkedbox", False)
            try:
                word_obj = WordList.objects.get(
                    category__recommended_by=user_obj, id=int(checked_word_id)
                )
                word_obj.delete()
                return redirect("portal:user_news_recommend_settings")
            except:
                return redirect("portal:user_news_recommend_settings")

    return render(
        request,
        "portal/user_news_recommend_settings.html",
        {
            "words": words,
            "categories": categories,
        },
    )


@login_required
def user_news_recommend_settings_category_manager(request):

    categories = Category.objects.all()

    if request.method == "POST":

        username = request.user.username
        user_obj = get_object_or_404(User, username=username)

        if "taskAdd" in request.POST:

            category_name = request.POST.get("description", False)

            if category_name != "":

                category_object = Category.objects.create(
                    recommended_by=user_obj, name=category_name
                )

                category_object.save()

                return redirect("portal:user_news_recommend_settings_category_manager")

            else:
                return redirect("portal:user_news_recommend_settings_category_manager")

        if "taskDelete" in request.POST:
            checked_category_id = request.POST.get("checkedbox", False)
            print(checked_category_id)
            try:
                category_obj = Category.objects.get(
                    recommended_by=user_obj, id=int(checked_category_id)
                )
                category_obj.delete()
                return redirect("portal:user_news_recommend_settings_category_manager")
            except:
                return redirect("portal:user_news_recommend_settings_category_manager")
    return render(
        request,
        "portal/user_news_recommend_settings_category_manager.html",
        {
            "categories": categories,
        },
    )


# ---------------------------------------Initial NewsAPI testing--------------------------------------
def AlJazeera(request):
    newsapi = NewsApiClient(
        api_key="cbdd86a002e24e569b7905729d546e91"
    )  #'<your api key>')
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")

    articles = topheadlines["articles"]

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles["title"])
        desc.append(myarticles["description"])
        img.append(myarticles["urlToImage"])

    mylist = zip(news, desc, img)

    return render(request, "portal/aljazeera.html", context={"mylist": mylist})


def BBC(request):
    newsapi = NewsApiClient(
        api_key="cbdd86a002e24e569b7905729d546e91"
    )  # '<your API key>')
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")

    articles = topheadlines["articles"]

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles["title"])
        desc.append(myarticles["description"])
        img.append(myarticles["urlToImage"])

    mylist = zip(news, desc, img)

    return render(request, "portal/bbc.html", context={"mylist": mylist})


# For 404 and 505 page handle
def handler404(request, template_name="../templates/404.html"):
    response = render(None, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="../templates/500.html"):
    response = render(None, template_name)
    response.status_code = 500
    return response
