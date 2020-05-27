from django.shortcuts import render

from workshops.models import Workshop


def catalog(request):
	return render(request, 'main/catalog.html', {
		'workshops': Workshop.objects.filter(active=True)
	})
