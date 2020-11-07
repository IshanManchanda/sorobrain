from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse

from quiz.models import Quiz
from .forms import AddUserForm, UpdateUserForm
from .models import User, BookAccess, OneOnOneClass
from .models.code import DiscountCode


def get_user_emails(modeladmin, request, queryset):
	emails = [user.email for user in queryset]
	string_emails = "".join([e + ", " for e in emails])
	request.session['_user_emails'] = string_emails
	return redirect(reverse('selected_emails'))


class UserAdmin(BaseUserAdmin):
	form = UpdateUserForm
	add_form = AddUserForm

	list_display = ('username', 'email', 'points', 'name', 'date_joined', 'is_staff')
	list_filter = ('is_staff', 'is_active', 'level', 'education', 'gender', 'notification_level', 'school', 'country')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'points', 'date_of_birth', 'phone', 'gender', 'level', 'education', 'school', 'city', 'country')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'notification_level', 'groups', 'user_permissions')}),
	)
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields': (
					'email', 'name', 'phone', 'gender', 'level', 'education', 'notification_level'
				)
			}
		),
	)
	search_fields = ('username', 'email', 'name', 'phone')
	ordering = ('username',)
	filter_horizontal = ('user_permissions', 'groups')
	actions = [get_user_emails]


admin.site.register(User, UserAdmin)


class BookAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'active', 'created_on')
	list_filter = ('active',)
	search_fields = ('user',)
	readonly_fields = ('created_on',)


admin.site.register(BookAccess, BookAccessAdmin)


class DiscountCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'uses', 'discount', 'content_type', 'content_object', 'expiry_date')
	list_filter = ('content_type',)
	search_fields = ('content_object',)
	readonly_fields = ('code', 'created_on')


admin.site.register(DiscountCode, DiscountCodeAdmin)


class OneOnOneClassAdmin(admin.ModelAdmin):
	list_display = ('title', 'cost', 'duo_cost', 'level', 'created_on')
	list_filter = ('level', 'active')
	search_fields = ('title',)
	list_editable = ('cost', 'duo_cost')
	readonly_fields = ('created_on', 'slug')


admin.site.register(OneOnOneClass, OneOnOneClassAdmin)
