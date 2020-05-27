from django.shortcuts import render, get_object_or_404
from django.views import View

from workshops.models import Workshop


class WorkshopStore(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		return render(request, 'workshops/workshop.html', {
			'workshop': w
		})
