from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from workshops.models import Workshop
from .utils import has_access_to_workshop


class WorkshopStore(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return redirect(reverse('workshops:workshop_access', args=[slug]))

		return render(request, 'workshops/workshop.html', {
			'workshop': w
		})


class HasAccessWorkshop(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return render(request, 'workshops/has_access_workshop.html', {
				'workshop': w
			})
		return render(request, 'global/message', {
			'message_title': 'No Permissions',
			'message'      : 'You do not have the permissions required to perform this action.'
		})
