from django.test import SimpleTestCase
from django.urls import reverse, resolve
from portal.views import (
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
	app_developer_app_update
)

class TestUrls (SimpleTestCase):

	def test_portal_admin_url_resolves(self):
		url = reverse('portal:portal-admin')
		found = resolve(url)
		self.assertEquals(found.func.view_class, DashboardAdminView)

	def test_admin_app_developer_list_url_resolves(self):
		url = reverse('portal:admin-app-developer-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, AdminAppDeveloperList)

	def test_admin_app_list_url_resolves(self):
		url = reverse('portal:admin-app-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, AdminAppList)

	def test_admin_app_user_list_resolves(self):
		url = reverse('portal:admin-app-user-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, AdminAppUserList)

	def test_app_developer_portal_url_resolves(self):
		url = reverse('portal:app-developer-portal')
		found = resolve(url)
		self.assertEquals(found.func.view_class, AppDeveloperView)
	
	def test_app_developer_profile_url_resolves(self):
		url = reverse('portal:app-developer-profile')
		found = resolve(url)
		self.assertEquals(found.func, app_developer_profile)
	"""
	def test_app_developer_home_app_list_url_resolves(self):
		url = reverse('portal:app-developer-home-app-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, app_developer_home_app_list)
	"""
	def test_app_developer_app_list_url_resolves(self):
		url = reverse('portal:app-developer-app-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, AppDeveloperAppView)
	
	def test_app_developer_app_upload_url_resolves(self):
		url = reverse('portal:app-developer-app-upload')
		found = resolve(url)
		self.assertEquals(found.func, app_developer_app_upload)
	
	def test_home_url_resolves(self):
		url = reverse('portal:home')
		found = resolve(url)
		self.assertEquals(found.func.view_class, HomeView)
	
	def test_user_profile_url_resolves(self):
		url = reverse('portal:user-profile')
		found = resolve(url)
		self.assertEquals(found.func, user_profile)
	
	def test_user_app_list_url_resolves(self):
		url = reverse('portal:user-app-list')
		found = resolve(url)
		self.assertEquals(found.func.view_class, UserAppView)

