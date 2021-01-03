from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from main.models.invoices import Invoice


def view_invoice(request, id):
	if not request.user.is_staff:
		return HttpResponse(403)
	invoice = get_object_or_404(Invoice, id=id)
	return render(request, 'main/actions/open_invoice.html', {
		'invoice': invoice,
	})
