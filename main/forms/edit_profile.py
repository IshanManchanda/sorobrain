from django import forms
from django.core.files.images import get_image_dimensions

from ..models import User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

GENDER_CHOICES = [
	('M', 'Male'),
	('F', 'Female'),
	('T', 'Transgender'),
	('O', 'Other'),
	('N', 'Prefer not say')
]

EDUCATION_CHOICES = [
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
	('fluent', 'Fluent/Native Speaker'),
	('advanced', 'Advanced'),
	('intermediate', 'Intermediate'),
	('beginner', 'Beginner')
]


class EditProfileForm(forms.Form):
	name = forms.CharField(label='Full name', required=True)
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES,
	                           required=False)
	phone = PhoneNumberField(label='Mobile Number', required=False,
	                         widget=PhoneNumberPrefixWidget)
	avatar = forms.ImageField(label='Profile Picture', required=False)
	education = forms.ChoiceField(label='Education level',
	                              choices=EDUCATION_CHOICES,
	                              required=False)
	level = forms.ChoiceField(label='French Fluency Level',
	                          choices=LEVEL_CHOICES,
	                          required=False)
