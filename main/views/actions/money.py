from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import User
from main.views.utils import give_soromoney_to_user


def give_soromoney_view(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		for user in users:
			give_soromoney_to_user(user, int(request.POST['amount']))
		messages.add_message(request, messages.SUCCESS, "Soromoney successfully given to users!")
		return redirect('/admin/main/user')

	return render(request, 'main/actions/give_soromoney.html', {
		'users': users,
	})
