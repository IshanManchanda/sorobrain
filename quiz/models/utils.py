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
	"""
	Checks if the answer from the user is any of the possible
	acceptable answers.
	"""
	cleaned_answer= selected_answer.strip().lower()
	cleaned_correct_answer_s = question.answer.strip().lower()

	correct_answers = [ans.strip() for ans in cleaned_correct_answer_s.split("|")]
	for correct_answer in correct_answers:
		if correct_answer == cleaned_answer:
			return True
	return False
