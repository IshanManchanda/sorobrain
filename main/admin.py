from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.models import ContentType

from quiz.models import Quiz
from .forms import AddUserForm, UpdateUserForm
from .models import User, BookAccess
from .models.code import DiscountCode


class UserAdmin(BaseUserAdmin):
	form = UpdateUserForm
	add_form = AddUserForm

	list_display = ('username', 'email', 'name', 'date_joined', 'is_staff')
	list_filter = ('is_staff', 'is_active')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'phone', 'gender', 'level', 'education')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'notification_level')}),
	)
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields': (
					'email', 'name', 'password1', 'password2'
				)
			}
		),
	)
	search_fields = ('username', 'email', 'name', 'phone')
	ordering = ('username',)
	filter_horizontal = ()
	readonly_fields = ('name', 'gender', 'email', 'phone', 'level', 'education', 'notification_level')


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
