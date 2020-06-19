def is_answer_valid(answer, question_type):
	if question_type == 'text':
		return True
	answer_options = ('T', 'F', '1', '2', '3', '4')
	if answer in answer_options:
		return True
	else:
		return False


def evaluate_mcq(question, selected_answer):
	if question.answer == selected_answer:
		return True
	elif selected_answer == "":
		return -1
	else:
		return False


def evaluate_bool(question, selected_answer):
	if question.answer.lower() == selected_answer.lower():
		return True
	elif selected_answer == "":
		return -1
	else:
		return False


def evaluate_text(question, selected_answer):
	cleaned_answer = selected_answer.strip().lower()
	cleaned_correct_answer = question.answer.strip().lower()
	if cleaned_answer == cleaned_correct_answer:
		return True
	elif selected_answer == "":
		return -1
	else:
		return False
