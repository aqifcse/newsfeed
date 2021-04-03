import datetime

from django.http import FileResponse, JsonResponse
from django.shortcuts import render, render_to_response
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


from .decorators import admin_required, app_user_required, app_developer_required
from .forms import UserSignUpForm, AppDeveloperSignUpForm, UserUpdateForm, UserLoginForm, AppDeveloperAppUploadForm, \
    AppDeveloperAppUpdateForm
from .models import User, App, AppDeveloper, AppUser, AppAuthor

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from portal.tokens import account_activation_token
from .serializers import UserUpdateSerializer, AppCreateUpdateSerializer

from pyaxmlparser import APK

# ------------------------------------------REST-framework-----------------------------------------
from rest_framework import viewsets, permissions, filters
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    lookup_field = 'username'


    def perform_update(self, serializer):
        username = self.kwargs.get('username')
        serializer.save(user=self.request.user)

        user = get_object_or_404(User, username = username)

        subject = 'Account Activation Status Mail from Team App Update Platform'
        current_site = get_current_site(self.request)
        sending_from = 'contact@kd.ticonsys.com'

        sending_to = user.email
        status = ''
        obj = ''
        instruction = ''

        if user.is_active == True:
            obj = 'App Developer account'
            instruction = 'Please login to http://ticonapp.com with your username and password'
            status = 'Activated'
        else:
            obj = 'App Developer account'
            instruction = 'Please contact admin for activation approval.'
            status = 'Deactivated'

        message = render_to_string('users/account_status_mail.html', {
            'user': user,
            'obj': obj,
            'status': status,
            'instruction': instruction
        })

        send_mail( subject, message, sending_from, [ sending_to ], fail_silently=False)


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'


class AppUpdateAPIView(RetrieveUpdateAPIView):
    queryset = App.objects.all()
    serializer_class = AppCreateUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        app_id = self.kwargs['pk']
        app = get_object_or_404(App, pk=app_id)
        developer = get_object_or_404(AppDeveloper, pk = app.app.author)
        user = get_object_or_404(User, username = developer.user.username)

        subject = 'App Activation Status Mail from Team App Update Platform'
        current_site = get_current_site(self.request)
        sending_from = 'contact@kd.ticonsys.com'

        sending_to = user.email
        status = ''
        obj = app.app.app_name + ' app '
        instruction = ''

        if app.is_active == True:
            instruction = 'The details of your app is given below'
            status = 'Activated'
        else:
            instruction = 'The details of your app is given below. Please contact the admin for your activation approval or you can go to your App Developer account and Activate it from your App List.'
            status = 'Deactivated'

        message = render_to_string('users/app_status_mail.html', {
            'user': user,
            'obj': obj,
            'status': status,
            'instruction': instruction,
            'app_name': app.app.app_name,
            'version_code': app.app_version_code,
            'version_name': app.app_version_name,
            'package_name': app.app_package_name,
            'downloads':app.downloads,
            'pub_date': app.pub_date,
        })

        send_mail( subject, message, sending_from, [ sending_to ], fail_silently=False)

    def get_queryset(self):
        app_id = self.kwargs['pk']
        app_name = get_object_or_404(App, pk=app_id)
        
        App.objects.filter(
            app__author__user__username=self.request.user, 
            app__app_name=app_name.app.app_name
        ).update(is_active=False)
        
        queryset = App.objects.all()
        return queryset

class AppDeleteAPIView(APIView):
    
    def post(self, request):
        entry_id = request.POST.get('app_name') # Here app_name in the AJAX hold the entry_id

        app = get_object_or_404(App, pk=entry_id)

        count = App.objects.filter(app__app_name = app).count() - 1 # By clicking delete button one count is already decreased
        
        if (count < 1): # When an app has no other instance lef but itself, excute the following
            App.objects.filter(id=entry_id).delete()
            AppAuthor.objects.filter(app_name = app).delete()  

        else: # If an app has other versions left
            App.objects.filter(id=entry_id).delete()
            # When a version of an App is deleted, the last inactive version will be activated 
            version = App.objects.filter(app__app_name=app)    
            last_version = 0
            for v in version:
                if last_version < v.app_version_code:
                    last_version = v.app_version_code
                v.save()
            App.objects.filter(app__app_name=app, app_version_code = last_version).update(is_active = True)

        return Response({
            'status': status.HTTP_202_ACCEPTED,
            'message': 'App deleted.'
        })

class AppVersionCheckAPIView(APIView):

    def get(self, request, format=None):
        
        app_package_name = request.GET.get('package_name')
        
        version = App.objects.filter(app_package_name=app_package_name, is_active=True)
        last_version = 0
        for v in version:
            if last_version < v.app_version_code:
                last_version = v.app_version_code
            v.save()

        data = App.objects.filter(
            app_package_name=app_package_name, 
            app_version_code=last_version,
        )

        modified_data = {
                'app_name': '',
                'current_version_code': 0,
                'current_version': '',
                'url': '',
                'notice': '',
                'release_note': '',
                'logo': ''
        }


        #current_site = 'http://13.229.180.187/media/'
        current_site = get_current_site(request)
        apk_path = 'http://' + current_site.domain + '/media'
        logo_path = 'http://' + current_site.domain + '/media/' 
        for i in data:
            modified_data = {
                'app_name': i.app.app_name,
                'current_version_code': i.app_version_code,
                'current_version': i.app_version_name,
                'url': apk_path + str(i.app_file),
                'notice': i.app_update_notice,
                'release_note': i.app_release_note,
                'logo': logo_path + str(i.app_logo)
            }

        return Response(modified_data)

class DownloadCountAPIView(APIView):

    queryset = App.objects.all()

    def get(self, request, *args, **kwargs):
        
        app_id = self.kwargs['pk']
        app_file = get_object_or_404(App, pk = app_id)

        download = app_file.downloads
        download = download + 1
        
        App.objects.filter(pk = app_id).update(downloads=download)

        data = {
            'count' : download
        }
        
        return Response(data)

# class UploadYearSelectAPIView(APIView):
    
#     def get(self, request, *args, **kwargs):
        
#         year = request.GET.get('get_selected_upload_year')

#         if year:
#             print(year)
            
#             monthly_upload_count_list = []

#             for i in range ( 1, 13 ):
#                 monthly_upload_count_list.append(App.objects.filter( pub_date__year = year, pub_date__month = i ).count())

#             data = {
#                 "count_list" : monthly_upload_count_list
#             }
#         else:
#             year = datetime.datetime.now().year

#         return Response(data)

# class DownloadYearSelectAPIView(APIView):

#     def get(self, request, *args, **kwargs):

#         year = request.GET.get('get_selected_download_year')

#         monthly_download_count_list = []

#         monthly_download_count = 0

#         for i in range ( 1, 13 ):
#             monthly_download_count = monthly_download_count_list.append(App.objects.filter( pub_date__year = year, pub_date__month = i ).count())

#         data = {
#             'download_count' : monthly_download_count
#         }

#         return Response(data)

# ------------------------------------------------------------------------End REST------------------------------------------------------------------------------------


class AppDeveloperSignUpView(CreateView):
    model = User
    form_class = AppDeveloperSignUpForm
    template_name = 'users/signup_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'user_type': 'App developer',
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save()
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your App Developer account in App Developer Platform'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, 'contact@kd.ticonsys.com')

            email_sent_message = 'An email has been sent to ' + str(user.email) + ' Please check your email and click on the confirmation link to confirm your account'

            return render(request, 'users/login.html', {
                'success_message': email_sent_message,
            })

        return render(request, self.template_name, {'form': form})


class AppUserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'users/signup_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'user_type': 'App User',
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your User account in App Developer Platform'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message, 'contact@kd.ticonsys.com')

            email_sent_message = 'An email has been sent to ' + str(user.email) + ' Please check your email and click on the confirmation link to confirm your account'

            return render(request, 'users/login.html', {
                'success_message': email_sent_message,
            })

        return render(request, self.template_name, {'form': form})

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


class MyLoginView(LoginView):
    form_class = UserLoginForm

    def get_success_url(self):
        if self.request.user.is_admin:
            return reverse('portal:portal-admin')
        elif self.request.user.is_developer:
            return reverse('portal:app-developer-portal')
        elif self.request.user.is_user:
            return reverse('portal:home')
        else:
            return reverse('portal:home')

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


class MyPasswordRestView(PasswordResetView):
    from_email = 'contact@kd.ticonsys.com'
    html_email_template_name = 'users/password_reset_email_template.html'
    subject_template_name = 'users/password_reset_subject.txt'
    template_name = 'users/password_reset.html'


@method_decorator([login_required, admin_required], name='dispatch')
class DashboardAdminView(ListView):
    model = User
    template_name = 'portal/admin_portal.html'
    context_object_name = 'apps'
    ordering = ['date']

    def get_queryset(self):
        total_download = App.objects.aggregate(Sum('downloads'))

        #year_list = list(range(1990, 2041, 1))

        queryset = {
            "total_upload" : App.objects.filter(is_active = True),
            "total_download": total_download['downloads__sum'],
            #"year_list": year_list
        }
        return queryset

    def get_context_data(self, **kwargs):

        today = datetime.date.today()

        kwargs['year'] = today.year

        kwargs['month_name'] = [
            'January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'Jun', 
            'July', 
            'August', 
            'September',
            'October', 
            'November', 
            'December'
        ]

        # Month Wise App Upload record sent to chartjs
        upload_count = []

        for i in range ( 1, 13 ):
            upload_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = i, is_active = True ).count())

        kwargs['upload_count'] = upload_count

        # Month Wise App Download record sent to chartjs
        download_count = []

        for j in range ( 1, 13 ):
            download_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = j ).aggregate(Sum('downloads')).get('downloads__sum', 0))
            
        kwargs['download_count'] = download_count

        return super().get_context_data(**kwargs)

class SignUpView(TemplateView):
    template_name = 'users/signup.html'


@method_decorator([login_required, app_user_required], name='dispatch')
class HomeView(ListView):
    model = App
    template_name = 'portal/user_portal.html'
    context_object_name = 'apps'

    def get_queryset(self):
        total_download = App.objects.aggregate(Sum('downloads'))

        #year_list = list(range(1990, 2041, 1))

        queryset = {
            "total_upload" : App.objects.filter(is_active = True),
            "total_download": total_download['downloads__sum'],
            #"year_list": year_list
        }
        return queryset

    def get_context_data(self, **kwargs):

        today = datetime.date.today()

        kwargs['year'] = today.year

        kwargs['month_name'] = [
            'January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'Jun', 
            'July', 
            'August', 
            'September',
            'October', 
            'November', 
            'December'
        ]

        # Month Wise App Upload record sent to chartjs
        upload_count = []

        for i in range ( 1, 13 ):
            upload_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = i, is_active = True ).count())

        kwargs['upload_count'] = upload_count

        # Month Wise App Download record sent to chartjs
        download_count = []

        for j in range ( 1, 13 ):
            download_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = j ).aggregate(Sum('downloads')).get('downloads__sum', 0))
            
        kwargs['download_count'] = download_count

        return super().get_context_data(**kwargs)



@method_decorator([login_required, app_developer_required], name='dispatch')
class AppDeveloperView(ListView):
    model = App
    template_name = 'portal/app_developer_portal.html'
    context_object_name = 'apps'

    def get_queryset(self):
        total_download = App.objects.aggregate(Sum('downloads'))

        #year_list = list(range(1990, 2041, 1))

        queryset = {
            "total_upload" : App.objects.filter(is_active = True),
            "total_download": total_download['downloads__sum'],
            #"year_list": year_list
        }
        return queryset

    def get_context_data(self, **kwargs):

        today = datetime.date.today()

        kwargs['year'] = today.year

        kwargs['month_name'] = [
            'January', 
            'February', 
            'March', 
            'April', 
            'May', 
            'Jun', 
            'July', 
            'August', 
            'September',
            'October', 
            'November', 
            'December'
        ]

        # Month Wise App Upload record sent to chartjs
        upload_count = []

        for i in range ( 1, 13 ):
            upload_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = i, is_active = True ).count())

        kwargs['upload_count'] = upload_count

        # Month Wise App Download record sent to chartjs
        download_count = []

        for j in range ( 1, 13 ):
            download_count.append(App.objects.filter( pub_date__year = today.year, pub_date__month = j ).aggregate(Sum('downloads')).get('downloads__sum', 0))
            
        kwargs['download_count'] = download_count

        return super().get_context_data(**kwargs)


@login_required
@admin_required
def admin_profile(request):
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
    return render(request, 'portal/admin_profile.html', context)


@login_required
@app_user_required
def user_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return render(request, 'portal/user_profile.html', {
                'u_form': u_form,
                'message': 'Your account has been updated!'
            })
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'portal/user_profile.html', context)


@login_required
@app_developer_required
def app_developer_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return render(request, 'portal/app_developer_profile.html', {
                'u_form': u_form,
                'message': 'Your account has been updated!'
            })
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    return render(request, 'portal/app_developer_profile.html', context)


@login_required
@app_developer_required
def app_developer_app_upload(request):
    if request.method == 'POST':
        aul_form = AppDeveloperAppUploadForm(request.POST, request.FILES, instance=request.user)
        try:
            author = request.user.username
            author_name = AppDeveloper.objects.get(user__username=author)

            if aul_form.is_valid():
                app_file = aul_form.cleaned_data['app_file']
                app_logo = aul_form.cleaned_data['app_logo']
                app_name = aul_form.cleaned_data['app_name']  
                app_version_name = aul_form.cleaned_data['app_version_name']
                app_short_description = aul_form.cleaned_data['app_short_description']
                app_long_description = aul_form.cleaned_data['app_long_description']
                app_release_note = aul_form.cleaned_data['app_release_note']
                app_update_notice = aul_form.cleaned_data['app_update_notice']
                

                if App.objects.filter(app__app_name = app_name).exists():
                    return render(request, 'portal/app_developer_app_upload.html', {
                        'aul_form': aul_form,
                        'message': 'App with the same app name already exist.'
                    })

                filetype = app_file.name
                if not filetype.endswith('.apk'):
                    return render(request, 'portal/app_developer_app_upload.html', {
                        'aul_form': aul_form,
                        'message': 'Please upload APK file.'
                    })

                fs = FileSystemStorage() 
                file = fs.save('apk/' + filetype, app_file) 
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
                fileurl = fs.url(file) 

                apk = APK(settings.BASE_DIR+fileurl)

                app_package_name = apk.package
                if App.objects.filter(app_package_name = app_package_name).exists():
                    return render(request, 'portal/app_developer_app_upload.html', {
                        'aul_form': aul_form,
                        'message': 'App with the same package name already exist.'
                    })

                app_version_code = int(apk.version_code)

                AppAuthor.objects.create(author=author_name, app_name=app_name)
                app = AppAuthor.objects.get(app_name=app_name)

                App.objects.create(
                    app_file=fileurl.replace('/media',''),
                    app_logo=app_logo,
                    app=app, 
                    app_version_code=app_version_code, 
                    app_version_name=app_version_name, 
                    app_package_name=app_package_name, 
                    app_short_description=app_short_description, 
                    app_long_description=app_long_description,
                    app_release_note=app_release_note,
                    app_update_notice=app_update_notice,
                    
                )
                
                return redirect('portal:app-developer-app-list')
        
            if not aul_form.is_valid():
                return render(request, 'portal/app_developer_app_upload.html', {
                    'aul_form': aul_form,
                    'message': 'Form is invalid please check the inputs'
                })
        except:
            return render(request, 'portal/app_developer_app_upload.html', {
                'aul_form': aul_form,
                'message': 'Something is wrong with the entry data. Please check all the fields and your apk info again' 
            })
    else:
        aul_form = AppDeveloperAppUploadForm(instance=request.user)
        return render(request, 'portal/app_developer_app_upload.html', {
            'aul_form': aul_form
        })


@login_required
@app_developer_required
def app_developer_app_update(request):
    if request.method == 'POST':
        aud_form = AppDeveloperAppUpdateForm(request.POST, request.FILES, instance=request.user)
        try:
            author = request.user.username
            author_name = AppDeveloper.objects.get(user__username=author)
            if aud_form.is_valid():

                app_file = aud_form.cleaned_data['app_file']
                app_logo = aud_form.cleaned_data['app_logo']
                app_name = aud_form.cleaned_data['app']
                #app_version_code = aud_form.cleaned_data['app_version_code']
                app_version_name = aud_form.cleaned_data['app_version_name']
                app_short_description = aud_form.cleaned_data['app_short_description']
                app_long_description = aud_form.cleaned_data['app_long_description']
                app_release_note = aud_form.cleaned_data['app_release_note']
                app_update_notice = aud_form.cleaned_data['app_update_notice']

                filetype = app_file.name
                if not filetype.endswith('.apk'):
                    return render(request, 'portal/app_developer_app_update.html', {
                        'aud_form': aud_form,
                        'message': 'Please upload APK file.'
                    })

                fs = FileSystemStorage() 
                file = fs.save('apk/'+filetype, app_file) 
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
                fileurl = fs.url(file) 

                apk = APK(settings.BASE_DIR+fileurl)

                apk_package_name = apk.package


                app_version_code = int(apk.version_code)
                

                version = App.objects.filter(app__author=author_name, app__app_name=app_name)
                last_version = 0
                for v in version:
                    
                    if last_version < v.app_version_code:
                        last_version = v.app_version_code
                    v.save()

                if last_version >= app_version_code:
                    return render(request, 'portal/app_developer_app_update.html', {
                        'aud_form': aud_form,
                        'message': 'Please upload latest version of the App.'
                    })

                app_author = AppAuthor.objects.get(app_name=app_name)
                app = App.objects.filter(app = app_author.id).last()

                if not app_logo or app_logo==None:
                    app_logo = app.app_logo

                if not app.app_package_name == apk_package_name:
                    return render(request, 'portal/app_developer_app_update.html', {
                        'aud_form': aud_form,
                        'message': 'Package name mismatch!! Please select the .apk file with the same package name given in the uploaded apk file'
                    })
                App.objects.create(
                    app_file=str(fileurl).replace('/media',''),
                    app_logo=app_logo,
                    app=app_author, 
                    app_version_code=app_version_code, 
                    app_version_name=app_version_name, 
                    app_package_name=app.app_package_name, 
                    app_short_description=app_short_description, 
                    app_long_description=app_long_description,
                    app_release_note=app_release_note,
                    app_update_notice=app_update_notice,  
                )
                version = App.objects.filter(app__author=author_name, app__app_name=app_name, is_active=True)
                last_version = 0
                for v in version:
                    if v.app_version_code!=app_version_code:
                        v.is_active=False
                        v.save()

                return redirect('portal:app-developer-app-list')

            if not aud_form.is_valid():
                return render(request, 'portal/app_developer_app_update.html', {
                    'aud_form': aud_form,
                    'message': 'Only jpg or png is supported format for logo. The image file should be 512x512px shape'
                })
        except:
            return render(request, 'portal/app_developer_app_update.html', {
                'aud_form': aud_form,
                'message': 'Form Crashed'
            })
    else:
        aud_form = AppDeveloperAppUpdateForm(instance=request.user)
    return render(request, 'portal/app_developer_app_update.html', {
        'aud_form': aud_form
    })


@method_decorator([login_required, app_user_required], name='dispatch')
class UserAppView(ListView):
    model = App
    template_name = 'portal/user_app_list.html'
    context_object_name = 'apps'
    paginate_by = 5

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            )
        queryset = App.objects.filter(is_active=True).order_by('pub_date').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, app_user_required], name='dispatch')
class UserAppDetailsView(DetailView):
    model = App
    template_name = 'portal/user_app_details.html'

"""
@method_decorator([login_required, app_developer_required], name='dispatch')
class AppDeveloperHomeAppView(ListView):
    model = App
    template_name = 'portal/app_developer_home_app_list.html'
    context_object_name = 'apps'
    paginate_by = 5

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter( 
                Q(app_name__icontains=form) | Q(app_version__icontains=form) | Q(app_details__icontains=form)
            )
        queryset = App.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)
"""


@method_decorator([login_required, app_developer_required], name='dispatch')
class AppDeveloperAppView(ListView):
    model = App
    template_name = 'portal/app_developer_app_list.html'
    context_object_name = 'apps'
    paginate_by = 5

    def get_queryset(self):
        author = self.request.user.username
        author_name = AppDeveloper.objects.get(user__username=author)
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            )
        queryset = App.objects.filter(app__author=author_name).order_by('pub_date').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, app_developer_required], name='dispatch')
class AppDeveloperAppDetailsView(DetailView):
    model = App
    template_name = 'portal/app_developer_app_details.html'


@method_decorator([login_required, app_developer_required], name='dispatch')
class AppDeveloperAppUploadView(CreateView):
    model = App
    template_name = 'portal/app_developer_app_upload.html'


@method_decorator([login_required, admin_required], name='dispatch')
class AdminAppDeveloperList(ListView):
    model = AppDeveloper
    template_name = 'portal/admin_app_developer_list.html'
    context_object_name = 'app_developer'
    paginate_by = 5

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            )
        queryset = AppDeveloper.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)


@method_decorator([login_required, admin_required], name='dispatch')
class AdminAppList(ListView):
    model = App
    template_name = 'portal/admin_app_list.html'
    context_object_name = 'apps'
    paginate_by = 5

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return App.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            )
        queryset = App.objects.all().order_by('pub_date').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminAppUserList(ListView):
    model = AppUser
    template_name = 'portal/admin_user_list.html'
    context_object_name = 'app_user'
    paginate_by = 5

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return AppUser.objects.filter(
                Q(user__username__icontains=form) | 
                Q(user__email__icontains=form) | 
                Q(user__first_name__icontains=form) | 
                Q(user__last_name__icontains=form)
            )
        queryset = AppUser.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminAppDetailsView(DetailView):
    model = App
    template_name = 'portal/admin_app_details.html'


# For 404 and 505 page handle

def handler404(request, exception, template_name="../templates/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request, exception, template_name="../templates/500.html"):
    response = render_to_response(template_name)
    response.status_code = 500
    return response
