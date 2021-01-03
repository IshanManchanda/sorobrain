from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import User, ReferralCode
from main.views.utils import give_soromoney_to_user
from sorobrain.utils.utils import add_ledger_credit


def give_soromoney_view(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	usernames_string = request.session.get('_usernames')
	users = [get_object_or_404(User, username=u.strip()) for u in usernames_string.split(',')[:-1]]

	if request.method == 'POST':
		for user in users:
			give_soromoney_to_user(user, int(request.POST['amount']))
			add_ledger_credit(user, int(request.POST['amount']), "Admin Added Credit")
		messages.add_message(request, messages.SUCCESS, "Soromoney successfully given to users!")
		return redirect('/admin/main/user')

	return render(request, 'main/actions/give_soromoney.html', {
		'users': users,
	})


class RedeemReferralCode(LoginRequiredMixin, View): 
	@staticmethod
	def post(request):
		code = get_object_or_404(ReferralCode, code=request.POST.get('referral_code').strip())
		if code.code == request.user.referral_code.code:
			messages.add_message(request, messages.WARNING,
			"You cannot use your own code!")
			return redirect(reverse('profile'))
			
		if request.user in list(code.used_by.all()):
			messages.add_message(request, messages.WARNING,
			"You cannot use the same code more than once!")
			return redirect(reverse('profile'))
 
		code.use(request.user)

		messages.add_message(request, messages.SUCCESS,
		 f"""This referral code has been redeemed.
		  Re. {code.referee_incentive} has been added
		   to your SoroMoney balance.""")
		return redirect(reverse('profile'))


def update_incentive_view(request):
	if not request.user.is_staff:
		return HttpResponse(403)
	codes_string = request.session.get('_codes')
	print(codes_string)
	codes = [get_object_or_404(ReferralCode, id=int(c.strip())) for c in codes_string.split(',')[:-1]]

	if request.method == "POST":
		field = request.POST.get('field')
		amount = int(request.POST.get('amount'))
		for code in codes: 
			if field == "referrer":
				code.referrer_incentive = amount
			elif field == "referee":
				code.referee_incentive = amount
			elif field == "both":
				code.referrer_incentive = amount
				code.referee_incentive = amount
			code.save()
		messages.add_message(request, messages.SUCCESS, "Incentives successfully updated!")
		return redirect('/admin/main/referralcode')
	
	return render(request, 'main/actions/update_incentives.html', {
		'codes': codes,
	})
