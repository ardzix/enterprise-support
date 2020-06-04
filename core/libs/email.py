from django.shortcuts import reverse
from core.libs.generate_pdf import PA_pdf, MA_pdf

import json
from datetime import date
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import pre_save, post_save

from core.structures.authentication.models import User, EmailVerification, send_verification_email

def send_mail_with_attachment(subject_template_name, email_template_name, html_email_template_name,
              context, to_email, attachment, filename, from_email=None, mandrill_template=None, mandrill_variables=None,
              cc=[]):
    """
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    if not from_email:
        from_email = getattr(settings, 'FROM_EMAIL')

    subject = loader.render_to_string(subject_template_name, context)

    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    headers = {}

    if mandrill_template:
        headers["X-MC-Template"] = mandrill_template

    if mandrill_variables:
        headers["X-MC-MergeVars"] = json.dumps(mandrill_variables)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [to_email], headers=headers, cc=cc)

    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    

    email_message.attach(filename, attachment, 'application/pdf')

    email_message.send()



def application_submit_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_submit.txt'
    html_email_template_name = 'home/email/application_submit.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def application_approved_email(request, loan):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_approved.txt'
    html_email_template_name = 'home/email/application_approved.html'
    email_template_name = html_email_template_name

    email = loan.owned_by.email
    context = {
        'name' : loan.owned_by.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )
    offer_letter_email(request, loan)

def offer_letter_email(request, loan):
    # from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/offer_letter.txt'
    html_email_template_name = 'home/email/offer_letter.html'
    email_template_name = html_email_template_name
    pdf = MA_pdf(request, loan)

    context = {
        'name' : loan.owned_by.full_name
    }

    filename = "{date}-{name}-ma.pdf".format(
        date=date.today(),
        name=loan.owned_by.full_name,
    )

    email = loan.owned_by.email
    send_mail_with_attachment(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email,
        pdf,
        filename
    )

def application_rejected_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_rejected.txt'
    html_email_template_name = 'home/email/application_rejected.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def application_proceed_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_proceed.txt'
    html_email_template_name = 'home/email/application_proceed.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def application_unpublish_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_unpublish.txt'
    html_email_template_name = 'home/email/application_unpublish.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def application_disbursed_email(email, cc, loan):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/application_disburse.txt'
    html_email_template_name = 'home/email/application_disburse.html'
    email_template_name = html_email_template_name

    context = {
        'loan' : loan
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email,
        cc=cc
    )


def account_approved_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/account_approved.txt'
    html_email_template_name = 'home/email/account_approved.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def account_rejected_email(email, user, reason):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/account_rejected.txt'
    html_email_template_name = 'home/email/account_rejected.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name,
        'reason' : reason
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def account_submission_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/account_submission.txt'
    html_email_template_name = 'home/email/account_submission.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def account_submission_complete_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/account_submission_complete.txt'
    html_email_template_name = 'home/email/account_submission_complete.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def topup_requested_email(email, user, topup):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/topup_requested.txt'
    html_email_template_name = 'home/email/topup_requested.html'
    email_template_name = html_email_template_name

    profile = user.get_profile()
    show_bank_account = False
    if profile.approved_at and profile.type == 2:
        show_bank_account = True

    context = {
        'name' : user.full_name,
        'amount' : topup.get_formatted_amount(),
        'show_bank_account' : show_bank_account,
        'link' : '%saccount/wallet/topup/?inv=%s' % (
            settings.BASE_URL,
            topup.invoice.number)
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def topup_approved_email(email, user, topup):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/topup_approved.txt'
    html_email_template_name = 'home/email/topup_approved.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name,
        'amount' : topup.get_formatted_amount(),
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def topup_rejected_email(email, user, topup):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/topup_rejected.txt'
    html_email_template_name = 'home/email/topup_rejected.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name,
        'amount' : topup.get_formatted_amount(),
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def withdraw_approved_email(email, user, withdraw):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/withdraw_approved.txt'
    html_email_template_name = 'home/email/withdraw_approved.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name,
        'amount' : withdraw.get_formatted_amount(),
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def withdraw_rejected_email(email, user, withdraw):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/withdraw_rejected.txt'
    html_email_template_name = 'home/email/withdraw_rejected.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name,
        'amount' : withdraw.get_formatted_amount(),
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )


def funding_sent_email(request, email, user):
    # from enterprise.libs.email import send_mail
    from django.conf import settings
    from enterprise.libs.email import send_mail

    subject_template_name = 'home/email/funding_sent.txt'
    html_email_template_name = 'home/email/funding_sent.html'
    email_template_name = html_email_template_name
    # pdf = PA_pdf(request, user)

    context = {
        'name' : user.full_name,
    }

    filename = "{date}-{name}-pa.pdf".format(
        date=date.today(),
        name=user.full_name,
    )

    # send_mail_with_attachment(
    #     subject_template_name,
    #     email_template_name,
    #     html_email_template_name,
    #     context,
    #     email,
    #     pdf,
    #     filename
    # )


    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def repayment_email(email, cc, payment):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/repayment.txt'
    html_email_template_name = 'home/email/repayment.html'
    email_template_name = html_email_template_name

    context = {
        'payment' : payment,
        'loan' : payment.loan,
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email,
        cc=cc
    )

def user_created_by_admin_email(email, user):
    from enterprise.libs.email import send_mail
    from django.conf import settings

    subject_template_name = 'home/email/account_verification.txt'
    html_email_template_name = 'home/email/account_verification.html'
    email_template_name = html_email_template_name

    context = {
        'name' : user.full_name
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        email
    )

def bulk_upload_report(uploader, success, failed):
    from enterprise.libs.email import send_mail
    from django.conf import settings
    from core.libs.constant import ECOMMERCE

    subject_template_name = 'home/email/bulk_upload_report.txt'
    html_email_template_name = 'home/email/bulk_upload_report.html'
    email_template_name = html_email_template_name

    context = {
        'name' : uploader.full_name,
        'ecommerce' : dict(ECOMMERCE).get(uploader.get_profile().associated_with),
        'success' : success,
        'failed' : failed,
    }

    send_mail(
        subject_template_name,
        email_template_name,
        html_email_template_name,
        context,
        uploader.email
    )


@receiver(pre_save, sender=User)
def verify_email(sender, instance, **kwargs):
    from django.conf import settings
    from core.structures.authentication.models import User
    # import ipdb ; ipdb.set_trace()

    if getattr(settings, 'AUTO_VERIFY_EMAIL', False):
        email = instance.email
        if instance.is_sent_email:
            existed_user = User.objects.filter(id=instance.id).first()
            if not existed_user:
                send_verification_email(
                    email,
                    instance
                )
            else:
                if email != existed_user.email:
                    send_verification_email(email, instance)


@receiver(post_save, sender=User)
def save_ev(sender, instance, **kwargs):
    ev = EmailVerification.objects.filter(email=instance.email).last()
    if ev:
        ev.user = instance
        ev.save()