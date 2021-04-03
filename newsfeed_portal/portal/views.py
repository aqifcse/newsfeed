from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import is_safe_url
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, View
from django.db.models import Q


from .forms import UserAuthForm
from .models import News

from newsapi.newsapi_client import NewsApiClient



import datetime

from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Value, F, Sum
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, View
from django.views.generic.detail import DetailView
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage


# from .decorators import admin_required, app_user_required, app_developer_required
# from .forms import UserSignUpForm, AppDeveloperSignUpForm, UserUpdateForm, UserLoginForm, AppDeveloperAppUploadForm, \
#     AppDeveloperAppUpdateForm
# from .models import User, App, AppDeveloper, AppUser, AppAuthor

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from portal.tokens import account_activation_token
# from .serializers import UserUpdateSerializer, AppCreateUpdateSerializer

# ------------------------------------------REST-framework-----------------------------------------
from rest_framework import viewsets, permissions, filters
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserLoginView(LoginView):
    form_class = UserAuthForm

    def get_success_url(self):
        if self.request.user:
            return reverse('portal:user_home')
        else:
            return reverse('portal:user_home')

    def form_invalid(self, form):
        # error message
        error_messages = []
        message = form.errors.get_json_data()
        for _, message_value in message.items():
            error = message_value[0]['message']
            error_messages.append(error)
        message_ = ' And '.join(error_messages)

        # Check user_type
        user_type = 'asdfa'
        if user_type:
            messages.error(self.request, message_)
            return redirect('login')
        elif user_type:
            messages.error(self.request, message_)
            return redirect('login')
        return self.render_to_response(self.get_context_data(form=form))

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

class SignUpView(TemplateView):
    template_name = 'users/signup.html'

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
            if user.is_user:
                user.is_active = True
            elif user.is_developer:
                user.is_active = False

            user.email_confirmed = True
            user.save()
            login(request, user)

            if user.is_user:
                user_success_account_message = email_sent_message = 'Hi!! ' + str(user.username) + ' Your account have been confirmed. Please log with your given username and password.'

                return render(request, 'users/login.html', {
                    'success_message': user_success_account_message,
                })
            elif user.is_developer:
                admin_approval_message = 'Hi ' + str(user.username) +'!! Please wait for the activation status email from the admin. Once you get it, you will be able to login with your given username and password.  '
                return render(request, 'users/login.html', {
                    'success_message': admin_approval_message,
                })            
        else:
            return render(request, 'users/login.html', {
                'error_message': 'The confirmation link was invalid, possibly because it has already been used.'
            })

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = News
    template_name = 'users/user_home.html'
    context_object_name = 'records'
    paginate_by = 15
    
    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return News.objects.filter(
                Q(image_url__icontains=form) | 
                Q(result__icontains=form) |
                Q(created_at__icontains=form)
            )
        queryset = News.objects.all().order_by('created_at').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

class MyPasswordRestView(PasswordResetView):
    from_email = 'contact@kd.ticonsys.com'
    html_email_template_name = 'users/password_reset_email_template.html'
    subject_template_name = 'users/password_reset_subject.txt'
    template_name = 'users/password_reset.html'

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()       
            return render(request, 'portal/admin_profile.html', {
                'u_form': u_form,
                'message': 'Your account has been updated!'
            })
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'portal/profile.html', context)


def AlJazeera(request):
    newsapi = NewsApiClient(api_key='cbdd86a002e24e569b7905729d546e91')    #'<your api key>')
    topheadlines = newsapi.get_top_headlines(sources='al-jazeera-english')


    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])


    mylist = zip(news, desc, img)


    return render(request, 'al-jazeera.html', context={"mylist":mylist})

def BBC(request):
    newsapi = NewsApiClient(api_key='cbdd86a002e24e569b7905729d546e91')# '<your API key>')
    topheadlines = newsapi.get_top_headlines(sources='bbc-news')


    articles = topheadlines['articles']

    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])


    mylist = zip(news, desc, img)


    return render(request, 'bbc.html', context={"mylist":mylist})

# For 404 and 505 page handle
def handler404(request, template_name="../templates/404.html"):
    response = render(None, template_name)
    response.status_code = 404
    return response


def handler500(request, template_name="../templates/500.html"):
    response = render(None, template_name)
    response.status_code = 500
    return response
