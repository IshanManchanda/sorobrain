from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AddUserForm, UpdateUserForm
from .models import User, BookAccess


class UserAdmin(BaseUserAdmin):
	form = UpdateUserForm
	add_form = AddUserForm

	list_display = ('username', 'email', 'name', 'is_staff')
	list_filter = ('is_staff', 'is_active')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'phone')}),
		('Permissions', {'fields': ('is_active', 'is_staff')}),
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


admin.site.register(User, UserAdmin)


class BookAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'active', 'created_on')
	list_filter = ('active',)
	search_fields = ('user',)
	readonly_fields = ('created_on',)


admin.site.register(BookAccess, BookAccessAdmin)
