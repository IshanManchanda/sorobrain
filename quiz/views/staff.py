from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from quiz.models import Question


@require_http_methods(["GET"])
@staff_member_required
def question(request, question_id):
	q = get_object_or_404(Question, id=question_id)
	return render(request, 'quiz/staff/question.html', {
		'question': q
	})
