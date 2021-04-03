from django.urls import path, include

from .views import (
    HomeView, 
    DashboardAdminView, 
    user_profile, 
    AppDeveloperView,
    UserAppView, 
    app_developer_profile,  
    # AppDeveloperHomeAppView, #
    AppDeveloperAppView, 
    AppDeveloperAppUploadView, 
    app_developer_app_upload, 
    AdminAppDeveloperList,
    AdminAppList, 
    AdminAppUserList, 
    app_developer_app_update, 
    AdminAppDetailsView,
    admin_profile,
    AppDeveloperAppDetailsView,
    UserAppDetailsView 
)

app_name = 'portal'

urlpatterns = [
    # admin
    path('portal-admin/', DashboardAdminView.as_view(), name='portal-admin'),
    path('admin-app-developer-list/', AdminAppDeveloperList.as_view(), name='admin-app-developer-list'),
    path('admin-app-list/', AdminAppList.as_view(), name='admin-app-list'),
    path('admin-app-user-list/', AdminAppUserList.as_view(), name='admin-app-user-list'),
    path('admin-app-details/<pk>', AdminAppDetailsView.as_view(), name='admin-app-details'),
    path('admin-profile/', admin_profile, name='admin-profile'),
    # app_developer
    path('app-developer-portal/', AppDeveloperView.as_view(), name='app-developer-portal'),
    path('app-developer-profile/', app_developer_profile, name='app-developer-profile'),
    # path('app-developer-home-app-list/', AppDeveloperHomeAppView.as_view(), name='app-developer-home-app-list'),
    path('app-developer-app-list/', AppDeveloperAppView.as_view(), name='app-developer-app-list'),
    path('app-developer-app-upload/', app_developer_app_upload, name='app-developer-app-upload'),
    path('app-developer-app-update/', app_developer_app_update, name='app-developer-app-update'),
    path('app-developer-app-details/<pk>', AppDeveloperAppDetailsView.as_view(), name='app-developer-app-details'),
    # User
    path('', HomeView.as_view(), name='home'),
    path('user-profile/', user_profile, name='user-profile'),
    path('user-app-list/', UserAppView.as_view(), name='user-app-list'),
    path('user-app-details/<pk>', UserAppDetailsView.as_view(), name='user-app-details'),
]
