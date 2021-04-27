from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from competition.models import Competition
from competition.views.utils import grant_access_to_competition
from main.forms.actions import BulkCompetitionAccessForm
from main.models import User


def grant_competition_access(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		form = BulkCompetitionAccessForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			competitions = data['competitions']
			for user in users:
				for c in competitions:
					grant_access_to_competition(user, c)
		messages.add_message(request, messages.SUCCESS, "Access granted to users successfully!")
		return redirect('/admin/main/user')

	form = BulkCompetitionAccessForm()

	return render(request, 'main/actions/competition_access.html', {
		'form': form,
		'users': users,
		'competitions': Competition.objects.filter(active=True)
	})
