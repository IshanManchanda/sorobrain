from django.shortcuts import render
from django.views import View


def index(request):
	return render(request, 'main/index.html')


class Book(View):
	@staticmethod
	def get(request):
		return render(request, 'main/book.html', {})

	@staticmethod
	def post(request):
		pass