def is_answer_valid(answer, question_type):
	if question_type == 'text':
		return True
	answer_options = ('T', 'F', '1', '2', '3', '4')
	if answer in answer_options:
		return True
	else:
		return False
