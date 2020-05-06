from __future__ import unicode_literals

from datetime import date

from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from core.structures.loan.models import Loan, Fund, Payment, ParticipationAgreement
from core.structures.account.models import Company

from enterprise.structures.transaction.models import BankAccount

from weasyprint import HTML, CSS

def UA_pdf(request, loan):
    company = loan.company
    bank = BankAccount.objects.filter(owned_by=loan.owned_by).first()
    response = HttpResponse(content_type="application/pdf")

    # import ipdb ; ipdb.set_trace()
    html_string = render_to_string("home/email/attachment/underlying-agreement.html", {
        'today': date.today(),
        'year': date.today().year,
        'loan': loan,
        'company': company,
        'bank': bank,
        'ma': loan.masteragreement_set.first()
    })
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    return pdf

def PA_pdf(request, pa):
    fund = pa.fund
    response = HttpResponse(content_type="application/pdf")

    # import ipdb ; ipdb.set_trace()
    html_string = render_to_string("home/email/attachment/participant-agreement.html", {
        'today': date.today(),
        'year': date.today().year,
        'fund': fund,
        'pa': pa,
    })
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    return pdf

def MA_pdf(request, loan):
    company = loan.company
    bank = BankAccount.objects.filter(owned_by=loan.owned_by).first()
    response = HttpResponse(content_type="application/pdf")

    # import ipdb ; ipdb.set_trace()
    html_string = render_to_string("home/email/attachment/master-agreement.html", {
        'today': date.today(),
        'year': date.today().year,
        'loan': loan,
        'company': company,
        'bank': bank,
        'ma': loan.masteragreement_set.first()
    })
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()

    return pdf