from django import forms
from django.core.files.images import get_image_dimensions
from django.forms import RadioSelect, DateInput, SelectDateWidget

from ..models import User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from sorobrain.utils.widgets import PictureWidget

GENDER_CHOICES = [
	(None, ''),  # show blank by default
	('M', 'Male'),
	('F', 'Female'),
	('N', 'Non Binary')
]

EDUCATION_CHOICES = [
	(None, ''),
	('working', 'Graduate or Higher'),
	('college', 'College'),
	('12', '12th Class'),
	('11', '11th Class'),
	('10', '10th Class'),
	('9', '9th Class'),
	('8', '8th Class'),
	('7', '7th Class'),
	('6', '6th Class'),
	('5', '5th Class'),
	('4', '4th Class'),
]

LEVEL_CHOICES = [
	(None, ''),
	('advanced', 'Advanced'),
	('intermediate', 'Intermediate'),
	('beginner', 'Beginner')
]

NOTIFICATION_LEVEL_CHOICES = [
	(0, 'Disable All Notifications'),
	(1, 'Email me only when its critical'),
	(2, 'Email me reminders and updates'),
	(3, 'Email me some promotions'),
	(4, 'Keep all notifications on')
]


class EditProfileForm(forms.Form):
	name = forms.CharField(label='Full name', required=True)
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES,
	                           required=False)
	date_of_birth = forms.DateField(label='Date of Birth', widget=forms.TextInput(attrs={'type': 'date'}))
	phone = PhoneNumberField(label='Mobile Number', required=False,
	                         widget=PhoneNumberPrefixWidget)
	avatar = forms.ImageField(label='Profile Picture', widget=PictureWidget,
	                          required=False)
	education = forms.ChoiceField(label='Education level',
	                              choices=EDUCATION_CHOICES,
	                              required=False)
	school = forms.CharField(label='School/College/Institute',)
	city = forms.CharField(label='City')
	country = forms.CharField(label='Country')


class UpdateNotification(forms.Form):
	notification_level = forms.ChoiceField(label='Notification Level',
	                                       choices=NOTIFICATION_LEVEL_CHOICES,
	                                       widget=RadioSelect,
	                                       required=False)
