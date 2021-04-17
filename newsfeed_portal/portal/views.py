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
import json

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

# -------------------------------------------REST APIs, Class based View, Function based View strts from here------------------------------------


class UserReadListTrackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get(
            "username", None
        )  # readlist_id in the AJAX hold the readlist_id

        input_key = request.data.get("key", None)
        input_timestamp = request.data.get("timestamp", None)

        client_message = str(input_timestamp) + "newsfeed"

        generated_signature_by_client = hashlib.sha256(
            client_message.encode()
        ).hexdigest()

        event_status_code = 0

        timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

        if username is not None or not username == "":
            if generated_signature_by_client == input_key:

                if (
                    timestamp_now <= int(input_timestamp) + 360000000
                ):  # Setting the sigtnature expiration time to 360000000 seconds or 100 hour. If needed, cange the expiration time as you wish

                    if not User.objects.filter(username=username).exists():
                        event_status_code = 0
                        status_message = ["User doesn't exist"]

                    else:
                        user_obj = get_object_or_404(User, username=username)
                        readlist_objs = ReadList.objects.filter(created_by=user_obj)

                        readlists = []
                        readlist_news_bodies = []

                        readlist_data = {
                            "id": "",
                            "keyword": "",
                            "source": "",
                            "country": "",
                            "top_headlines_url": "",
                            "full_stories_url": "",
                            "newsletter": "",
                            "created_at": "",
                        }

                        readlist_news_body_data = {
                            "id": "",
                            "readlist": "",
                            "headline": "",
                            "thumbnail": "",
                            "source_of_news": "",
                            "country_of_news": "",
                            "original_news_source_link": "",
                            "published_at": "",
                        }

                        for readlist_obj in readlist_objs:
                            readlist_data = {
                                "id": readlist_obj.id,
                                "keyword": readlist_obj.keyword,
                                "source": readlist_obj.source,
                                "country": readlist_obj.country,
                                "top_headlines_url": readlist_obj.top_headlines_url,
                                "full_stories_url": readlist_obj.full_stories_url,
                                "newsletter": readlist_obj.newsletter,
                                "created_at": readlist_obj.created_at,
                            }

                            # print(readlist_data)

                            readlists.append(readlist_data)

                            readlist_news_body_objs = ReadListNewsBody.objects.filter(
                                readlist=readlist_obj
                            )

                            for readlist_news_body_obj in readlist_news_body_objs:
                                readlist_news_body_data = {
                                    "id": readlist_news_body_obj.id,
                                    "keyword": readlist_news_body_obj.readlist.keyword,
                                    "headline": readlist_news_body_obj.headline,
                                    "thumbnail": readlist_news_body_obj.thumbnail,
                                    "source_of_news": readlist_news_body_obj.source_of_news,
                                    "country_of_news": readlist_news_body_obj.country_of_news,
                                    "original_news_source_link": readlist_news_body_obj.original_news_source_link,
                                    "published_at": readlist_news_body_obj.published_at,
                                }

                                readlist_news_bodies.append(readlist_news_body_data)

                        data = {
                            "username": user_obj.username,
                            "first_name": user_obj.first_name,
                            "last_name": user_obj.last_name,
                            "subscribed": user_obj.subscribe,
                            "readlists": readlists,
                            "curated_news": readlist_news_bodies,
                        }
                        event_status_code = 1
                        return Response({"status": event_status_code, "result": data})

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


class SubscribeUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get(
            "username", None
        )  # readlist_id in the AJAX hold the readlist_id

        is_active = request.data.get(
            "is_active", None
        )  # is_active in the AJAX holds the is_active

        input_key = request.data.get("key", None)
        input_timestamp = request.data.get("timestamp", None)

        client_message = str(input_timestamp) + "newsfeed"

        generated_signature_by_client = hashlib.sha256(
            client_message.encode()
        ).hexdigest()

        event_status_code = 0

        timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))

        if username is not None or not username == "":
            if generated_signature_by_client == input_key:

                if (
                    timestamp_now <= int(input_timestamp) + 360000000
                ):  # Setting the sigtnature expiration time to 360000000 seconds or 100 hour. If needed, cange the expiration time as you wish

                    if not User.objects.filter(username=username).exists():
                        event_status_code = 0
                        status_message = ["User doesn't exist"]

                    else:
                        user_obj = get_object_or_404(User, username=username)
                        user_obj.subscribe = is_active
                        user_obj.save()

                        event_status_code = 1
                        message = (
                            "Success !! Subscribe activation status is set to -> "
                            + is_active
                            + " for USER ID : "
                            + username
                        )
                        status_message = [message]

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

        is_active = request.data.get(
            "is_active", None
        )  # is_active in the AJAX holds the is_active

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
                        or not is_active
                        or is_active == ""
                    ):
                        event_status_code = 0
                        status_message = [
                            "readlist_id doesn't exist or is_active is null"
                        ]

                    else:
                        ReadList.objects.filter(id=int(readlist_id)).update(
                            newsletter=is_active
                        )
                        event_status_code = 1
                        message = (
                            "Success !! Newsletter activation status is set to "
                            + is_active
                        )
                        status_message = [message]

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
                    timestamp_now <= int(input_timestamp) + 36000000
                ):  # Setting the sigtnature expiration time to 360000 seconds or 100 hour

                    if not ReadList.objects.filter(pk=readlist_id).exists():
                        event_status_code = 0
                        status_message = ["readlist_id doesn't exist"]

                    else:
                        readlist = get_object_or_404(ReadList, pk=readlist_id)
                        if not ReadListNewsBody.objects.filter(
                            readlist=readlist
                        ).exists():
                            ReadList.objects.filter(id=int(readlist_id)).delete()
                            event_status_code = 1
                            status_message = [
                                "There is no ReadListNewsBody found in this ReadList. Only readlist item successfully Deleted!!"
                            ]
                        else:
                            ReadListNewsBody.objects.filter(readlist=readlist).delete()
                            ReadList.objects.filter(id=int(readlist_id)).delete()
                            event_status_code = 1
                            status_message = [
                                "Both ReadListNewsBody and ReadList are successfully Deleted!!"
                            ]

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
    # print(data)
    context = {"success": True, "data": [], "search": search}

    # seprating the necessary data
    for i in data:
        context["data"].append(
            {
                "title": i["title"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "source": i["source"]["name"],
                # "country": i["source"]["country"],
                "publishedat": i["publishedAt"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
            }
        )
    # send the news feed to template in context
    return render(request, "portal/user_home.html", context=context)


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
                    country = ""
                if not source or source == None:
                    source = ""
                if not keyword or keyword == None:
                    keyword = ""

                page = 1
                # user preffered top headlines

                top_headlines_url = "https://newsapi.org/v2/top-headlines?q={}&country={}&source={}&page={}&apiKey={}".format(
                    keyword, country, source, page, settings.APIKEY
                )

                full_stories_url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
                    keyword, "popularity", page, settings.APIKEY
                )

                ReadList.objects.create(
                    created_by=user_obj,
                    keyword=keyword,
                    country=country,
                    source=source,
                    top_headlines_url=top_headlines_url,
                    full_stories_url=full_stories_url,
                )

                readlist = ReadList.objects.get(created_by=user_obj, keyword=keyword)

                full_stories_resp = requests.get(url=full_stories_url)

                full_stories_data = full_stories_resp.json()

                full_stories_data = full_stories_data["articles"]

                # seprating the necessary full_stories_data
                for i in full_stories_data:
                    ReadListNewsBody.objects.create(
                        readlist=readlist,
                        headline=i["title"],
                        thumbnail=temp_img
                        if i["urlToImage"] is None
                        else i["urlToImage"],
                        source_of_news="" if source is None else source,
                        country_of_news="" if country is None else country,
                        original_news_source_link=i["url"],
                        published_at=i["publishedAt"],
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
                    Q(keyword__icontains=form)
                    | Q(source__icontains=form)
                    | Q(country__icontains=form)
                )
                .order_by("created_at")
                .reverse()
            )
        queryset = ReadList.objects.all().order_by("created_at").reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs["q"] = self.request.GET.get("q")
        return super().get_context_data(**kwargs)


@login_required
def user_top_headlines(request, pk):

    readlist_obj = get_object_or_404(ReadList, keyword=pk)
    top_headlines_url = readlist_obj.top_headlines_url
    print("Full Stories : " + top_headlines_url)

    top_headlines_resp = requests.get(url=top_headlines_url)

    search = readlist_obj.keyword
    print("Search : " + search)

    top_headlines_data = top_headlines_resp.json()
    # print(top_headlines_data["articles"])

    if top_headlines_data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")

    top_headlines_data = top_headlines_data["articles"]

    top_headlines_context = {
        "success": True,
        "data": [],
        "search": search,
    }
    # seprating the necessary top_headlines_data
    for i in top_headlines_data:
        top_headlines_context["data"].append(
            {
                "title": i["title"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"],
            }
        )
    # print(top_headlines_context)
    # send the news feed to template in context
    return render(
        request,
        "portal/user_top_headlines.html",
        context=top_headlines_context,
    )


@login_required
def user_full_stories(request, pk):

    readlist_obj = get_object_or_404(ReadList, keyword=pk)
    full_stories_url = readlist_obj.full_stories_url
    print("Full Stories : " + full_stories_url)

    full_stories_resp = requests.get(url=full_stories_url)

    search = readlist_obj.keyword
    print("Search : " + search)

    full_stories_data = full_stories_resp.json()
    # print(full_stories_data["articles"])

    if full_stories_data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")

    full_stories_data = full_stories_data["articles"]

    full_stories_context = {
        "success": True,
        "data": [],
        "search": search,
    }
    # seprating the necessary full_stories_data
    for i in full_stories_data:
        full_stories_context["data"].append(
            {
                "title": i["title"],
                "description": "" if i["description"] is None else i["description"],
                "url": i["url"],
                "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                "publishedat": i["publishedAt"],
            }
        )
    # print(full_stories_context)
    # send the news feed to template in context
    return render(
        request,
        "portal/user_full_stories.html",
        context=full_stories_context,
    )


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
        # print("url:", url)
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
                    "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
                    # "source": "" if i["source"]["name"] is None else i["source"]["id"],
                    # "country": i["source"]["country"],
                    "publishedat": i["publishedAt"],
                    "description": "" if i["description"] is None else i["description"],
                    "url": i["url"],
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