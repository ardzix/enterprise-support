'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: core.bimaasia.id
# File Created: Wednesday, 24th April 2019 11:13:10 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 24th April 2019 11:13:10 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import datetime
import calendar
from numpy import ipmt, ppmt, pmt
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from enterprise.structures.common.models import File
from enterprise.structures.common.models.base import BaseModelGeneric, BaseModelUnique
from core.structures.authentication.models import User as U
from enterprise.structures.transaction.models import BankAccount
from enterprise.libs import storage
from enterprise.libs import base36
from enterprise.libs.moment import to_timestamp

from core.libs import constant
from core.structures.account.models import Company, Address, Profile, ECommerce
from core.structures.borrower.models import Guarantee, Financial, SocialMedia


User = settings.AUTH_USER_MODEL


class Grade(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    interest_min = models.DecimalField(decimal_places=3, max_digits=3)
    interest_max = models.DecimalField(decimal_places=3, max_digits=3)

    def __str__(self):
        return '%s (%s-%s)' % (
            self.display_name,
            self.get_interest_min_str(),
            self.get_interest_max_str()
        )

    def get_interest_min_str(self):
        return '%s%%' % ('{:.2f}'.format(self.interest_min * 100))

    def get_interest_max_str(self):
        return '%s%%' % ('{:.2f}'.format(self.interest_max * 100))

    class Meta:
        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')


class LoanType(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    display_name_id = models.CharField(
        max_length=150, verbose_name="Display Name (id)")
    short_name = models.SlugField(max_length=150)
    group_type = models.PositiveIntegerField(
        choices=constant.LOAN_TYPE_CHOICES)
    thumbnail = models.ImageField(
        storage=storage.LOGO_STORAGE,
        max_length=300
    )

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Loan Type')
        verbose_name_plural = _('Loan Types')


class DocumentKey(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    display_name_id = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    loan_type = models.ForeignKey(
        LoanType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Document Key')
        verbose_name_plural = _('Document Keys')


class DetailKey(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    display_name_id = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    description_id = models.TextField(blank=True, null=True)
    loan_type = models.ForeignKey(
        LoanType, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Detail Key')
        verbose_name_plural = _('Detail Keys')


class FactSheetKey(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    display_name_id = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    loan_group_type = models.PositiveIntegerField(
        choices=constant.LOAN_TYPE_CHOICES)

    def __str__(self):
        return self.display_name

    def get_group(self):
        return dict(constant.LOAN_TYPE_CHOICES).get(self.loan_group_type)

    class Meta:
        verbose_name = _('FactSheet Key')
        verbose_name_plural = _('FactSheet Keys')


class FinancialSheetGroup(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('FinancialSheet Group')
        verbose_name_plural = _('FinancialSheet Groups')


class FinancialSheetKey(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    display_name_id = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(
        FinancialSheetGroup, on_delete=models.CASCADE, blank=True, null=True)
    loan_group_type = models.PositiveIntegerField(
        choices=constant.LOAN_TYPE_CHOICES)
    data_type = models.PositiveIntegerField(
        choices=constant.FINANCIAL_DATATYPE_CHOICES)

    def __str__(self):
        return self.display_name

    def get_group(self):
        return dict(constant.LOAN_TYPE_CHOICES).get(self.loan_group_type)

    def get_data_type(self):
        return dict(constant.FINANCIAL_DATATYPE_CHOICES).get(self.data_type)

    class Meta:
        verbose_name = _('FinancialSheet Key')
        verbose_name_plural = _('FinancialSheet Keys')


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


class Loan(BaseModelGeneric):
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE,)
    number = models.CharField(max_length=20)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(default='requested', max_length=40,
                              choices=constant.PROJECT_STATUS_CHOICES)

    bussiness = models.ForeignKey(Company, on_delete=models.CASCADE,
                                  blank=True, null=True)
    ecommerce = models.ForeignKey(ECommerce, on_delete=models.CASCADE,
                                  blank=True, null=True)
    attachements = models.ManyToManyField(File, blank=True)

    duration = models.PositiveIntegerField(default=1)
    admin_fee = models.DecimalField(choices=constant.ADMIN_FEE_CHOICES,
                                    decimal_places=2, max_digits=2, default=0.00)
    interest = models.DecimalField(
        decimal_places=3, max_digits=3, blank=True, null=True)

    score = models.DecimalField(
        decimal_places=0, max_digits=4, blank=True, null=True)

    crm_approved_at = models.DateTimeField(blank=True, null=True)
    crm_approved_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    crm_approved_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                        related_name="%(app_label)s_%(class)s_crm_approved_by")

    crm_unapproved_at = models.DateTimeField(blank=True, null=True)
    crm_unapproved_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    crm_unapproved_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                          related_name="%(app_label)s_%(class)s_crm_unapproved_by")

    disbursed_date = models.DateField(blank=True, null=True)
    disbursed_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='%(app_label)s_%(class)s_disbursed_by')
    fundraising_end_date = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.number

    def get_funds(self):
        return getattr(self, 'fund_set')

    def get_fund_amount(self):
        if self.get_funds().count() > 0:
            return self.get_funds().aggregate(
                models.Sum('amount'))['amount__sum']
        else:
            return 0

    def get_amount_remaining(self):
        return self.amount - self.get_fund_amount()

    def get_progress(self):
        if self.amount == 0 or self.get_fund_amount() == 0:
            return None
        return self.get_fund_amount() / self.amount

    def get_progress_str(self):
        if not self.get_progress():
            return '-'
        return '%s%%' % ('{:.2f}'.format(self.get_progress() * 100))

    def get_status(self):
        return dict(constant.PROJECT_STATUS_CHOICES)[self.status]

    def get_admin_fee(self):
        return '%s' % dict(constant.ADMIN_FEE_CHOICES)[self.admin_fee]

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    def get_formatted_fund_amount(self):
        return 'Rp.{:,.0f},-'.format(self.get_fund_amount())

    def get_interest_str(self):
        if not self.interest:
            return '-'
        return '%s%%' % ('{:.2f}'.format(self.interest * 100))

    def get_lender_interest_str(self):
        if not self.interest:
            return '-'
        return '%s%%' % ('{:.2f}'.format(self.lender_interest * 100))

    def get_funding_remaining(self):
        if not self.fundraising_end_date:
            return -1
        return (self.fundraising_end_date - datetime.date.today()).days

    def get_funding_remaining_str(self):
        if self.get_funding_remaining() < 0:
            return "N.A."
        return '%d day(s) to go' % self.get_funding_remaining()

    def get_funding_remaining_str_id(self):
        if self.get_funding_remaining() < 0:
            return "Belum Tersedia"
        return '%d hari lagi' % self.get_funding_remaining()

    def get_number(self):
        return '%s-%s' % (self.owned_by.get_profile().get_number(), self.number)

    def disburse(self, user=None, date=None, *args, **kwargs):
        if user:
            # mark when the record deleted
            self.disbursed_date = date if date else datetime.date.today()
            self.disbursed_by = user

            # save it
            return super().save(*args, **kwargs)

    def crm_approve(self, user=None, *args, **kwargs):
        if user:
            # mark when the record deleted
            self.crm_unapproved_at = None
            self.crm_unapproved_at_timestamp = None
            self.crm_unapproved_by = None
            self.crm_approved_at = timezone.now()
            self.crm_approved_at_timestamp = to_timestamp(self.crm_approved_at)
            self.crm_approved_by = user

            # save it
            return super().save(*args, **kwargs)

    def crm_reject(self, user=None, *args, **kwargs):
        if user:
            # mark when the record reovered
            self.crm_approved_at = None
            self.crm_approved_at_timestamp = None
            self.crm_approved_by = None
            self.crm_unapproved_at = timezone.now()
            self.crm_unapproved_at_timestamp = to_timestamp(
                self.crm_unapproved_at)
            self.crm_unapproved_by = user

            # save it
            return super().save(*args, **kwargs)

    def create_number(self, *args, **kwargs):
        if not self.number and self.pk:
            existing_loan_count = Loan.objects.filter(
                owned_by=self.owned_by).exclude(number="").count()
            number = 1 + existing_loan_count
            number = str(number).zfill(3)
            prefix = 'KUR'
            self.number = '{}-{}'.format(prefix, number)
            self.save()

    def generate_repayment(self):
        rate = self.interest/12
        if not self.lender_interest:
            self.lender_interest = self.interest
            self.save()
        lender_rate = self.lender_interest/12
        per = list(range(1, self.duration+1))
        nper = self.duration
        pv = self.amount

        calculated_principal = pv/nper
        calculated_pmt = abs(pmt(rate, nper, pv))
        calculated_lender_pmt = abs(pmt(lender_rate, nper, pv))
        calculated_interest = calculated_pmt - calculated_principal
        calculated_lender_interest = calculated_lender_pmt - calculated_principal

        # calculated_ipmt = ipmt(rate, per, nper, pv)
        # calculated_lender_ipmt = ipmt(lender_rate, per, nper, pv)
        # calculated_ppmt = ppmt(rate, per, nper, pv)
        # calculated_lender_ppmt = ppmt(lender_rate, per, nper, pv)

        # flat
        for x in range(self.duration):
            Payment.objects.create(
                loan=self,
                payment_order=per[x],
                created_by=self.created_by,
                due_date=add_months(datetime.date.today(), x + 1),
                interest_amount=calculated_interest,
                interest_lender_amount=calculated_lender_interest,
                principal_amount=calculated_principal,
                principal_lender_amount=calculated_principal,
                amount=calculated_pmt,
                lender_amount=calculated_lender_pmt
            )
        # effective
        # for x in range(self.duration):
        #     Payment.objects.create(
        #         loan=self,
        #         payment_order=per[x],
        #         created_by=self.created_by,
        #         due_date=add_months(datetime.date.today(), x + 1),
        #         interest_amount=abs(calculated_ipmt[x]),
        #         interest_lender_amount=abs(calculated_lender_ipmt[x]),
        #         principal_amount=abs(calculated_ppmt[x]),
        #         principal_lender_amount=abs(calculated_lender_ppmt[x]),
        #         amount=abs(calculated_ipmt[x]) + abs(calculated_ppmt[x]),
        #         lender_amount=abs(
        #             calculated_lender_ipmt[x]) + abs(calculated_lender_ppmt[x])
        #     )

        return self.payment_set.all()

    def save(self, create_number=True, *args, **kwargs):
        su = super().save(*args, **kwargs)
        if create_number:
            self.create_number()
        return su

    class Meta:
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')


class LoanDetail(BaseModelGeneric):
    key = models.SlugField(max_length=150)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    description_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.key, self.description)

    def get_key_str(self):
        return str(DetailKey.objects.filter(short_name=self.key).last())

    def get_key_str_id(self):
        return str(DetailKey.objects.filter(short_name=self.key).last().display_name_id)

    class Meta:
        verbose_name = _('Loan Detail')
        verbose_name_plural = _('Loan Details')


class FactSheet(BaseModelGeneric):
    key = models.SlugField(max_length=150)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    description_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.key, self.description)

    def get_key_str(self):
        return str(FactSheetKey.objects.filter(short_name=self.key).last())

    def get_key_str_id(self):
        return str(FactSheetKey.objects.filter(short_name=self.key).last().display_name_id)

    class Meta:
        verbose_name = _('Loan FactSheet')
        verbose_name_plural = _('Loan FactSheets')


class FinancialSheet(BaseModelGeneric):
    key = models.SlugField(max_length=150)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    group = models.ForeignKey(
        FinancialSheetGroup, on_delete=models.CASCADE, blank=True, null=True)
    data_type = models.PositiveIntegerField(
        choices=constant.FINANCIAL_DATATYPE_CHOICES)
    fiscal_min_1 = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    fiscal_min_2 = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    fiscal_min_3 = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    score = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s: %s' % (self.key, self.get_data_type())

    def get_data_type(self):
        return dict(constant.FINANCIAL_DATATYPE_CHOICES).get(self.data_type)

    def get_key_str(self):
        return str(FinancialSheetKey.objects.filter(short_name=self.key).last())

    def get_key_str_id(self):
        return str(FinancialSheetKey.objects.filter(short_name=self.key).last().display_name_id)

    class Meta:
        verbose_name = _('Loan FinancialSheet')
        verbose_name_plural = _('Loan FinancialSheets')


class ARPAnalysis(BaseModelGeneric):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=150)
    group = models.PositiveIntegerField(choices=constant.ARP_ANALYSIS_CHOICES)
    month_1 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_2 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_3 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_4 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_5 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_6 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_7 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_8 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_9 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_10 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_11 = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    month_12 = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    def __str__(self):
        return '%s - %s' % (self.group, self.display_name)

    def get_group(self):
        return dict(constant.ARP_ANALYSIS_CHOICES).get(self.group)

    class Meta:
        verbose_name = _('Account Receivable and Payable Analysis')
        verbose_name_plural = _('Account Receivable and Payable Analysis')


class LoanDocument(BaseModelGeneric):
    key = models.SlugField(max_length=150)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    document = models.FileField(
        max_length=300,
        storage=storage.FILE_STORAGE,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)
    description_id = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key

    def get_document(self):
        if self.document:
            return self.document.url
        else:
            return None

    def get_key_str(self):
        return str(DocumentKey.objects.filter(short_name=self.key).last())

    def get_key_str_id(self):
        return str(DocumentKey.objects.filter(short_name=self.key).last().display_name_id)

    class Meta:
        verbose_name = _('Loan Document')
        verbose_name_plural = _('Loan Documents')
        ordering = ['key']


class Fund(BaseModelGeneric):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.PositiveIntegerField(
        default=1, choices=constant.PAYMENT_STATUS_CHOICES)
    attachments = models.ManyToManyField(File, blank=True)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.get_formatted_amount()

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    def get_number(self):
        return '%s-%s' % (self.loan.get_number(), self.number)

    def create_number(self):
        if not self.number and self.pk:
            existing_fund_count = Fund.objects.filter(
                loan=self.loan).exclude(number="").count()
            number = 1 + existing_fund_count
            number = str(number).zfill(4)
            self.number = number
            self.save()

    def save(self, create_number=True, *args, **kwargs):
        su = super().save(*args, **kwargs)
        if create_number:
            self.create_number()
        return su

    class Meta:
        verbose_name = _('Fund')
        verbose_name_plural = _('Funds')


class Payment(BaseModelGeneric):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=0)
    interest_lender_amount = models.DecimalField(
        max_digits=12, decimal_places=0)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=0)
    principal_lender_amount = models.DecimalField(
        max_digits=12, decimal_places=0)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    lender_amount = models.DecimalField(max_digits=12, decimal_places=0)
    payment_order = models.PositiveIntegerField(default=1)
    due_date = models.DateField()
    paid_at = models.DateTimeField(blank=True, null=True)
    penalty = models.DecimalField(
        decimal_places=3, max_digits=3, default=0)
    status = models.CharField(
        max_length=40, choices=constant.PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return '%s:%s' % (self.loan.__str__(), self.due_date)

    def get_status(self):
        status = dict(constant.PAYMENT_STATUS_CHOICES)[self.status]
        if self.paid_at and self.paid_at.date() > self.due_date and self.status == 'paid':
            status = 'Delayed Paid'
        return status

    def get_formatted_interest_amount(self):
        return 'Rp.{:,.0f},-'.format(self.interest_amount)

    def get_formatted_interest_lender_amount(self):
        return 'Rp.{:,.0f},-'.format(self.interest_lender_amount)

    def get_formatted_principal_amount(self):
        return 'Rp.{:,.0f},-'.format(self.principal_amount)

    def get_formatted_principal_lender_amount(self):
        return 'Rp.{:,.0f},-'.format(self.principal_lender_amount)

    def get_formatted_amount(self):
        return 'Rp.{:,.0f},-'.format(self.amount)

    def get_formatted_lender_amount(self):
        return 'Rp.{:,.0f},-'.format(self.lender_amount)

    def pay(self):
        from decimal import Decimal
        from enterprise.libs.payment.wallet import get_balance, transfer_wallet

        admin_user = U.objects.filter(email='admin@bimaasia.id').first()
        if not admin_user:
            admin_user = U.objects.first()

        balance_to_be_transfered = self.amount + (self.amount * self.penalty)
        lender_balance_to_be_transfered = self.lender_amount + \
            (self.lender_amount * self.penalty)

        errors = []

        try:
            transfer_wallet(
                self.owned_by,
                admin_user,
                balance_to_be_transfered,
                obj=self,
                description='Repayment of loan: %s to Bima' % (self.loan.__str__()))
        except Exception as e:
            print(e)
            errors.append(e)

        for fund in self.loan.get_funds().all():
            fund_percentage = Decimal(fund.amount)/Decimal(self.loan.amount)
            lender_payment = fund_percentage * lender_balance_to_be_transfered

            try:
                transfer_wallet(
                    admin_user,
                    fund.owned_by,
                    lender_payment,
                    obj=self,
                    description='Repayment of loan: %s to %s' % (
                        self.loan.__str__(),
                        fund.owned_by.__str__()
                    )
                )
            except Exception as e:
                print(e)
                errors.append(e)

        self.status = 'paid'
        self.save()

        return errors

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')


class MasterAgreement(BaseModelGeneric):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('MasterAgreement')
        verbose_name_plural = _('MasterAgreements')

    def create_number(self, *args, **kwargs):
        if not self.number:
            number = 1
            last_ma = MasterAgreement.objects.filter(
                created_at__year=datetime.date.today().year
            ).last()
            if last_ma:
                number += last_ma.number
            self.number = number

    def save(self, *args, **kwargs):
        self.create_number()
        return super().save(*args, **kwargs)


class ParticipationAgreement(BaseModelGeneric):
    ma = models.ForeignKey(MasterAgreement, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=True, null=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('ParticipationAgreement')
        verbose_name_plural = _('ParticipationAgreements')

    def create_number(self, *args, **kwargs):
        if not self.number:
            number = 1
            last_pa = ParticipationAgreement.objects.filter(
                ma=self.ma,
                created_at__year=datetime.date.today().year
            ).last()
            if last_pa:
                number += last_pa.number
            self.number = number

    def save(self, *args, **kwargs):
        self.create_number()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=Loan)
def generate_ma(sender, instance, created, **kwargs):
    # from core.libs.agreement import generate_ma as f
    # f(instance)
    if created:
        # assign bussiness
        bussiness = Company.objects.filter(
            nonce=instance.nonce, deleted_at__isnull=True).last()
        instance.bussiness = bussiness
        # assign ecommerce
        ecommerce = ECommerce.objects.filter(
            nonce=instance.nonce, deleted_at__isnull=True).last()
        instance.ecommerce = ecommerce
        # assign documents
        files = File.objects.filter(
            nonce=instance.nonce, deleted_at__isnull=True)
        instance.attachements.set(files)
        instance.save()


# @receiver(post_save, sender=Fund)
# def generate_pa(sender, instance, **kwargs):
#     from core.libs.agreement import generate_pa as f
#     f(instance)
