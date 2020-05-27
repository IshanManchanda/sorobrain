from django.contrib import admin

from workshops.models import Workshop


class WorkshopAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'cost', 'discount', 'created_on')
	list_filter = ('active', 'include_book',)
	search_fields = ('title', 'description', 'zoom_link')
	readonly_fields = ('slug',)


admin.site.register(Workshop, WorkshopAdmin)
