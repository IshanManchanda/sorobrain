from main.models import User


def user_profile_setup_progress(user: User) -> int:
	empty_fields = 0
	if user.gender is None:
		empty_fields += 1
	if user.phone is None:
		empty_fields += 1
	# ignoring user.avatar as it is not essential for profile setup
	if user.education is None:
		empty_fields += 1
	if user.level is None:
		empty_fields += 1

	return empty_fields
