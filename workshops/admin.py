from django.contrib import admin

from workshops.models import Workshop, WorkshopAccess


class WorkshopAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'cost', 'discount', 'created_on')
	list_filter = ('active', 'include_book',)
	search_fields = ('title', 'description', 'zoom_link')
	readonly_fields = ('slug',)


class WorkshopAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'workshop', 'created_on')
	list_filter = ('workshop', 'active')
	search_fields = ('user', 'workshop')
	readonly_fields = ('created_on',)


admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopAccess, WorkshopAccessAdmin)
