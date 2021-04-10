import datetime

from .forms import *
from .models import *
from newsfeed_portal.settings import *
from .tokens import account_activation_token

# from .serializers import *

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

from django.http import FileResponse, JsonResponse, HttpResponse

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

import hashlib  # For Authentication

# ------------------------------------------NewsAPI-------------------------------------------------
from newsapi.newsapi_client import NewsApiClient
import requests

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

# -------------------------------------------REST APIs, Class based View, Function based View strts from here------------------------------------


class SubscribeUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        readlist_id = request.data.get(
            "readlist_id", None
        )  # readlist_id in the AJAX hold the readlist_id

        subscribeActiveStatus = request.data.get(
            "subscribeActiveStatus", None
        )  # subscribeActiveStatus in the AJAX holds the subscribeActiveStatus

        input_key = request.data.get("key", None)
        input_timestamp = request.data.get("timestamp", None)

        client_message = str(input_timestamp) + "newsfeed"

        generated_signature_by_client = hashlib.sha256(
            client_message.encode()
        ).hexdigest()

        event_status_code = 0

        timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

        if readlist_id is not None or not readlist_id == "":
            if generated_signature_by_client == input_key:

                if (
                    timestamp_now <= int(input_timestamp) + 360000
                ):  # Setting the sigtnature expiration time to 360000 seconds or 100 hour. If needed, cange the expiration time as you wish

                    if not ReadList.objects.filter(pk=readlist_id).exists():
                        event_status_code = 0
                        status_message = ["readlist_id doesn't exist"]

                    else:
                        created_by = ReadList.objects.filter(pk=readlist_id).values(
                            "created_by"
                        )
                        print(created_by.username)
                        User.objects.filter(username=created_by.username).update(
                            subscribe=subscribeActiveStatus
                        )
                        event_status_code = 1
                        status_message = ["Success!! Subscribe Updated"]

                else:
                    event_status_code = 0
                    status_message = ["Signature Expired"]
            else:
                event_status_code = 0
                status_message = ["Authentication Failure"]
        else:
            event_status_code = 0
            status_message = ["No Readlist Id is given in the input"]

        return Response({"status": event_status_code, "result": status_message})


class NewsLetterUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        readlist_id = request.data.get(
            "readlist_id", None
        )  # Here readlist in the AJAX hold the readlist_id

        newsLetterActiveStatus = request.data.get(
            "newsLetterActiveStatus", None
        )  # newsLetterActiveStatus in the AJAX holds the newsLetterActiveStatus

        input_key = request.data.get("key", None)
        input_timestamp = request.data.get("timestamp", None)

        client_message = str(input_timestamp) + "newsfeed"

        generated_signature_by_client = hashlib.sha256(
            client_message.encode()
        ).hexdigest()

        event_status_code = 0

        timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

        if readlist_id is not None or not readlist_id == "":
            if generated_signature_by_client == input_key:

                if (
                    timestamp_now <= int(input_timestamp) + 360000
                ):  # Setting the sigtnature expiration time to 360000 seconds or 100 hour. Cange the expiration time as you wish

                    if (
                        not ReadList.objects.filter(pk=readlist_id).exists()
                        or not newsLetterActiveStatus
                        or newsLetterActiveStatus == ""
                    ):
                        event_status_code = 0
                        status_message = [
                            "readlist_id doesn't exist or newsLetterActiveStatus is null"
                        ]

                    else:
                        ReadList.objects.filter(id=int(readlist_id)).update(
                            newsletter=newsLetterActiveStatus
                        )
                        event_status_code = 1
                        status_message = ["Newsletter Status updated Successfully!!"]

                else:
                    event_status_code = 0
                    status_message = ["Signature Expired"]
            else:
                event_status_code = 0
                status_message = ["Authentication Failure"]
        else:
            event_status_code = 0
            status_message = ["No Readlist Id is given in the input"]

        return Response({"status": event_status_code, "result": status_message})


class ReadListDeleteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        readlist_id = request.data.get(
            "readlist_id", None
        )  # Here readlist in the AJAX hold the readlist_id

        input_key = request.data.get("key", None)
        input_timestamp = request.data.get("timestamp", None)

        client_message = str(input_timestamp) + "newsfeed"

        generated_signature_by_client = hashlib.sha256(
            client_message.encode()
        ).hexdigest()

        event_status_code = 0

        timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

        if readlist_id is not None or not readlist_id == "":
            if generated_signature_by_client == input_key:

                if (
                    timestamp_now <= int(input_timestamp) + 360000
                ):  # Setting the sigtnature expiration time to 360000 seconds or 100 hour

                    if not ReadList.objects.filter(pk=readlist_id).exists():
                        event_status_code = 0
                        status_message = ["readlist_id doesn't exist"]

                    else:
                        ReadList.objects.filter(id=int(readlist_id)).delete()
                        event_status_code = 1
                        status_message = ["ReadList item successfully Deleted!!"]

                else:
                    event_status_code = 0
                    status_message = ["Signature Expired"]
            else:
                event_status_code = 0
                status_message = ["Authentication Failure"]
        else:
            event_status_code = 0
            status_message = ["No Readlist Id is given in the input"]

        return Response({"status": event_status_code, "result": status_message})


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


# @login_required
# def user_create_readlist(request):

# countries = Country.objects.all()
# sources = Source.objects.all()
# keywords = Keyword.objects.all()

# if request.method == "POST":

#     username = request.user.username
#     user_obj = get_object_or_404(User, username=username)

#     if "taskAdd" in request.POST:
#         country = request.POST.get("country", False)
#         source = request.POST.get("source", False)
#         keyword = request.POST.get("keyword", False)

#         if (
#             not country
#             or not source
#             or not keyword
#             or country == ""
#             or source == ""
#             or keyword == ""
#         ):
#             return redirect("portal:user_create_readlist")
#         else:
#             country_object = Country.objects.create(
#                 recommended_by=user_obj, country=country
#             )

#             sources_object = Source.objects.create(
#                 recommended_by=user_obj, source=source
#             )

#             keyword_object = Keyword.objects.create(
#                 recommended_by=user_obj, keyword=keyword
#             )

#             return redirect("portal:user_create_readlist")

#             # page = request.GET.get("page", 1)
#             # search = request.GET.get("search", None)

#             # if search is None or search == "top":
#             #     # get the top news
#             #     url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
#             #         "us", 1, settings.APIKEY
#             #     )
#             # else:
#             #     # get the search query request
#             #     url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
#             #         search, "popularity", page, settings.APIKEY
#             #     )
#             # r = requests.get(url=url)

#             # data = r.json()
#             # if data["status"] != "ok":
#             #     return HttpResponse("<h1>Request Failed</h1>")
#             # data = data["articles"]
#             # context = {"success": True, "data": [], "search": search}
#             # # seprating the necessary data
#             # for i in data:
#             #     context["data"].append(
#             #         {
#             #             "title": i["title"],
#             #             "description": ""
#             #             if i["description"] is None
#             #             else i["description"],
#             #             "url": i["url"],
#             #             "image": temp_img
#             #             if i["urlToImage"] is None
#             #             else i["urlToImage"],
#             #             "publishedat": i["publishedAt"],
#             #         }
#             #     )

#             # # send the news feed to template in context
#             # return render(
#             #     request, "portal/user_create_readlist.html", context=context
#             # )

#     if "taskDelete" in request.POST:
#         task_id = request.POST.get("checked_all", False)
#         try:
#             country_obj = Country.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             country_obj.delete()

#             source_obj = Source.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             source_obj.delete()

#             keyword_obj = Keyword.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             keyword_obj.delete()

#             return redirect("portal:user_create_readlist")
#         except:
#             return redirect("portal:user_create_readlist")

# return render(
#     request,
#     "portal/user_create_readlist.html",
#     {
#         "countries": countries,
#         "sources": sources,
#         "keywords": keywords,
#     },
# )
@login_required
def user_create_readlist(request):
    if request.method == "POST":
        nr_form = ReadListForm(request.POST, request.FILES, instance=request.user)
        try:
            username = request.user.username
            user_obj = get_object_or_404(User, username=username)

            if nr_form.is_valid():
                country = nr_form.cleaned_data["country"]
                source = nr_form.cleaned_data["source"]
                keyword = nr_form.cleaned_data["keyword"]

                if not country or country == None:
                    messages.error(
                        request, "Insert country of news", extra_tags="country_empty"
                    )
                    return render(
                        request,
                        "portal/user_create_readlist.html",
                        {"nr_form": nr_form},
                    )

                if not source or source == None:
                    messages.error(
                        request, "Insert source of news", extra_tags="source_empty"
                    )
                    return render(
                        request,
                        "portal/user_create_readlist.html",
                        {"nr_form": nr_form},
                    )

                if not keyword or keyword == None:
                    messages.error(
                        request, "Insert keyword of news", extra_tags="keyword_empty"
                    )
                    return render(
                        request,
                        "portal/user_create_readlist.html",
                        {"nr_form": nr_form},
                    )

                ReadList.objects.create(
                    created_by=user_obj,
                    country=country,
                    source=source,
                    keyword=keyword,
                )

                return redirect("portal:user_manage_readlists")

            else:
                messages.error(request, "Invalid Input", extra_tags="form_invalid")
                return render(
                    request,
                    "portal/user_create_readlist.html",
                    {"nr_form": nr_form},
                )

        except:
            messages.error(request, "Form Crashed", extra_tags="form_crashed")
            return render(
                request,
                "portal/user_create_readlist.html",
                {"nr_form": nr_form},
            )
    else:
        nr_form = ReadListForm(instance=request.user)
        return render(
            request,
            "portal/user_create_readlist.html",
            {"nr_form": nr_form},
        )


@method_decorator([login_required], name="dispatch")
class ManageReadListsView(ListView):
    model = ReadList
    template_name = "portal/user_manage_readlists.html"
    context_object_name = "readlists"
    paginate_by = 1

    def get_queryset(self):
        form = self.request.GET.get("q")
        if form:
            return (
                ReadList.objects.filter(
                    Q(country__icontains=form)
                    | Q(source__icontains=form)
                    | Q(keyword__icontains=form)
                )
                .order_by("created_at")
                .reverse()
            )
        queryset = ReadList.objects.all().order_by("created_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


def global_home(request):
    page = request.GET.get("page", 1)
    search = request.GET.get("search", None)

    if search is None or search == "top":
        # get the top news
        url = (
            "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us", 1, settings.APIKEY
            )
        )
    else:
        # get the search query request
        url = (
            "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search, "popularity", page, settings.APIKEY
            )
        )
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {"success": True, "data": [], "search": search}
    # seprating the necessary data
    for i in data:
        context["data"].append(
            {
                "title": i["title"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"],
            }
        )

    # send the news feed to template in context
    return render(request, "portal/global_home.html", context=context)


@login_required
def user_home(request):
    page = request.GET.get("page", 1)
    search = request.GET.get("search", None)

    if search is None or search == "top":
        # get the top news
        url = (
            "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us", 1, settings.APIKEY
            )
        )
    else:
        # get the search query request
        url = (
            "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search, "popularity", page, settings.APIKEY
            )
        )
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {"success": True, "data": [], "search": search}
    # seprating the necessary data
    for i in data:
        context["data"].append(
            {
                "title": i["title"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"],
            }
        )
    # send the news feed to template in context
    return render(request, "portal/user_home.html", context=context)


# For content latest news within 15 minutes
def loadcontent(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("search", None)
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        #     "Technology","popularity",page,settings.APIKEY
        # )
        if search is None or search == "top":
            url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
                "us", page, settings.APIKEY
            )
        else:
            url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                search, "popularity", page, settings.APIKEY
            )
        print("url:", url)
        r = requests.get(url=url)

        data = r.json()
        if data["status"] != "ok":
            return JsonResponse({"success": False})
        data = data["articles"]
        context = {"success": True, "data": [], "search": search}
        for i in data:
            context["data"].append(
                {
                    "title": i["title"],
                    "description": "" if i["description"] is None else i["description"],
                    "url": i["url"],
                    "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                    "publishedat": i["publishedAt"],
                }
            )

        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({"success": False})


# For 404 and 505 page handle
def handler404(request, template_name="../templates/404.html"):
    response = render(None, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="../templates/500.html"):
    response = render(None, template_name)
    response.status_code = 500
    return response