from django.contrib.sitemaps import Sitemap

from quiz.models import Quiz


class QuizSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.7

	def items(self):
		return Quiz.objects.all()

	def lastmod(self, obj):
		return obj.created_on
