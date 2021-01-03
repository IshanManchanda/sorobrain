from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views.actions.competition import grant_competition_access
from .views.actions.invoice import view_invoice
from .views.actions.money import give_soromoney_view, RedeemReferralCode, update_incentive_view
from .views.actions.quiz import grant_quiz_access
from .views.actions.workshop import grant_workshop_access


urlpatterns = [
	# admin extend
	path('selected_emails/', views.selected_emails, name="selected_emails"),
	path('grant_competition_access/', grant_competition_access, name="grant_competition_access"),
	path('grant_quiz_access/', grant_quiz_access, name="grant_quiz_access"),
	path('grant_workshop_access/', grant_workshop_access, name="grant_workshop_access"),
	path('give_soromoney/', give_soromoney_view, name="give_soromoney"),
	path('update_incentives/', update_incentive_view, name="update_incentive"),
	path('view_invoice/<int:id>/', view_invoice, name="view_invoice"),

	path('referral/', RedeemReferralCode.as_view(), name="referral"),

	# account
	path('accounts/profile/', views.Profile.as_view(), name='profile'),
	path('accounts/settings/', views.Settings.as_view(), name='settings'),
	path('accounts/delete/', views.Delete.as_view(), name='delete'),
	path('accounts/save_profile/', views.SaveProfileData.as_view(), name='save_profile'),
	path('accounts/save_notification', views.SaveNotificationLevel.as_view(), name='save_notifications'),
	path('register/', views.register, name='register'),

	path('class/<str:slug>/', views.ClassStore.as_view(), name='class'),

	path('book/', views.Book.as_view(), name='book'),
	path('book/success/', csrf_exempt(views.BookSuccess.as_view()), name='book_success'),

	path('catalog/', views.catalog, name='catalog'),
	path('all_competitions/', views.ViewAllCompetitions.as_view(), name='all_competitions'),
	path('all_quizzes/', views.ViewAllQuizzes.as_view(), name='all_quizzes'),
	path('all_workshops/', views.ViewAllWorkshops.as_view(), name='all_workshops'),

	path('privacy/', TemplateView.as_view(template_name='main/privacy.html'), name='privacy'),
	path('refund/', TemplateView.as_view(template_name='main/refund.html'), name='refund'),
	path('contact/', TemplateView.as_view(template_name='main/contact.html'), name='contact'),
	path('global/', TemplateView.as_view(template_name='main/global.html'), name='global'),
	path('reviews/', TemplateView.as_view(template_name='main/reviews.html'), name='reviews'),
	path('faq/', TemplateView.as_view(template_name='main/faq.html'), name='faq'),
	path('team/', TemplateView.as_view(template_name='main/team.html'), name='team'),

	path('', views.index, name='index'),
]
