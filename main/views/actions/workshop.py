from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import User
from workshops.models import Workshop
from workshops.views.utils import grant_access_to_workshop


def grant_workshop_access(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		w = get_object_or_404(Workshop, id=request.POST.get('workshop_id'))
		for user in users:
			grant_access_to_workshop(user, w)
		messages.add_message(request, messages.SUCCESS, "Access granted to users successfully!")
		return redirect('/admin/main/user')

	return render(request, 'main/actions/workshop_access.html', {
		'users': users,
		'workshops': Workshop.objects.filter(active=True)
	})
