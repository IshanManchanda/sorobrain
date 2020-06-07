from django.contrib.sitemaps import Sitemap

from workshops.models import Workshop


class WorkshopSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.7

	def items(self):
		return Workshop.objects.all()

	def lastmod(self, obj):
		return obj.created_on
