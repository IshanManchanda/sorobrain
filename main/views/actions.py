from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from competition.models import Competition
from competition.views.utils import grant_access_to_competition
from main.models import User
from quiz.models import Quiz
from quiz.views.utils import grant_access_to_quiz


def grant_competition_access(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		c = get_object_or_404(Competition, id=request.POST.get('competition_id'))
		for user in users:
			grant_access_to_competition(user, c)
		messages.add_message(request, messages.SUCCESS, "Access granted to users successfully!")
		return redirect('/admin/main/user')

	return render(request, 'main/actions/competition_access.html', {
		'users': users,
		'competitions': Competition.objects.filter(active=True)
	})


def grant_quiz_access(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		q = get_object_or_404(Quiz, id=request.POST.get('quiz_id'))
		for user in users:
			grant_access_to_quiz(user, q)
		messages.add_message(request, messages.SUCCESS, "Access granted to users successfully!")
		return redirect('/admin/main/user')

	return render(request, 'main/actions/quiz_access.html', {
		'users': users,
		'quizzes': Quiz.objects.filter(active=True)
	})
