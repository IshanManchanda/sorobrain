from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from ..forms import RegisterForm


@require_http_methods(['GET', 'POST'])
def register(request):
	if request.method == 'GET':
		form = RegisterForm()
		return render(request, 'main/register.html', {'form': form})

	form = RegisterForm(request.POST)
	if form.is_valid():
		form.save()
		# Send mail
		messages.success(request, 'Account created successfully')
		return redirect('login')

	return render(request, 'main/register.html', {'form': form})
