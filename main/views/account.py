from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from main.forms.edit_profile import EditProfileForm, UpdateNotification
from main.views.utils import user_profile_setup_progress, has_book_access
from workshops.models import WorkshopAccess


class Profile(LoginRequiredMixin, View):
	def get(self, request):
		empty_fields = user_profile_setup_progress(request.user)
		if empty_fields > 0:
			messages.add_message(request, messages.INFO, f"Finish setting up your profile <a href={reverse('settings')}> here</a>. You have {empty_fields} fields to fill.")
		return render(request, 'main/profile.html', {
			'access_workshops': WorkshopAccess.objects.filter(user=request.user),
			'has_book_access': has_book_access(user=request.user)
		})


class Settings(LoginRequiredMixin, View):
	permission_denied_message = "Please login or signup before coming here!"

	def get(self, request):
		user = request.user
		form = EditProfileForm(initial={
			'username': user.username,
			'email': user.email,
			'name': user.name,
			'gender': user.gender,
			'phone': user.phone,
			'avatar': user.avatar,
			'education': user.education,
			'level': user.level,
		})

		empty_fields = user_profile_setup_progress(user)
		if empty_fields > 0:
			messages.add_message(request, messages.INFO, f'Complete profile setup below! {empty_fields} fields to fill.')

		notification_form = UpdateNotification(initial={
			'notification_level': user.notification_level
		})

		return render(request, 'main/settings.html', {
			'form': form,
			'notification_form': notification_form,
		})


class SaveProfileData(LoginRequiredMixin, View):
	def post(self, request):
		user = request.user
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			data = form.cleaned_data
			user.name = data['name']
			user.gender = data['gender']
			user.phone = data['phone']
			user.avatar = data['avatar']
			user.education = data['education']
			user.level = data['level']
			user.save()

		messages.add_message(request, messages.SUCCESS, '<i class="fas fa-check"></i> Profile Successfully Updated!')
		return redirect(reverse('settings'))


class SaveNotificationLevel(LoginRequiredMixin, View):
	@staticmethod
	def post(request):
		user = request.user
		form = UpdateNotification(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user.notification_level = data['notification_level']
			user.save()

		messages.add_message(request, messages.SUCCESS, '<i class="fas fa-check"></i> Notification Level Successfully Updated!')
		return redirect(reverse('settings'))


class Delete(LoginRequiredMixin, View):
	permission_denied_message = "Please login or signup before coming here!"

	@staticmethod
	def get(request):
		return render(request, 'main/delete.html')

	@staticmethod
	def post(request):
		user = request.user
		# REVIEW:
		#  Currently instead of deleting a user, we are making it
		#  inactive as recommended in the docs s.t. f_keys don't break,
		#  but this means that we always maintain user data.
		#  Is this what we want?
		user.is_active = False
		user.save()
		logout(request)
		messages.add_message(request, messages.INFO, 'Your account has been deleted successfully.')
		return redirect(reverse('index'))
