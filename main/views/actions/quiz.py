from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import User
from quiz.models import Quiz
from quiz.views.utils import grant_access_to_quiz


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
