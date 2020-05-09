from random import randint
from datetime import date
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from enterprise.structures.common.models import File
from enterprise.structures.common.models.base import BaseModelGeneric, BaseModelUnique
from core.structures.authentication.models import User, EmailVerification
from enterprise.libs import storage

from core.libs import constant

User = settings.AUTH_USER_MODEL


class NonceWhiteList(models.Model):
    nonce = models.CharField(max_length=128)

    def __str__(self):
        return self.nonce

    class Meta:
        verbose_name = _('Nonce WhiteList')
        verbose_name_plural = _('Nonce WhiteList')


class Branch(models.Model):
    region = models.CharField(max_length=4)
    number = models.CharField(max_length=4)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')


class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')


class Regency(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Regency')
        verbose_name_plural = _('Regencies')


class Address(BaseModelGeneric):
    name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=3, choices=constant.COUNTRY_CHOICES,
                               default='IDN')
    timezone = models.CharField(max_length=48, blank=True, null=True)
    point = geo.PointField(blank=True, null=True)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=True, null=True)
    regency = models.ForeignKey(
        Regency, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class Phone(BaseModelGeneric):
    name = models.CharField(max_length=40, default="Default")
    number = models.CharField(max_length=24)
    country = models.CharField(
        max_length=3,
        choices=constant.COUNTRY_CHOICES,
        default='IDN')
    is_available = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        return super(Phone, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')


class Profile(BaseModelUnique):
    gender = models.PositiveIntegerField(choices=constant.GENDER_CHOICES,
                                         default=1)
    background_cover = models.ImageField(
        storage=storage.COVER_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        storage=storage.AVATAR_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=40, blank=True, null=True)
    id_card = models.FileField(
        max_length=300,
        storage=storage.FILE_STORAGE,
        blank=True,
        null=True
    )
    id_card_selfie = models.FileField(
        max_length=300,
        storage=storage.FILE_STORAGE,
        blank=True,
        null=True
    )
    id_card_num = models.CharField(max_length=40, blank=True, null=True)
    npwp_num = models.CharField(max_length=40, blank=True, null=True)
    addresses = models.ManyToManyField(Address, blank=True)
    phones = models.ManyToManyField(Phone, blank=True)
    type = models.PositiveIntegerField(
        choices=constant.PROFILE_TYPE_CHOICES, default=3)
    reject_reason = models.PositiveIntegerField(
        choices=constant.PROFILE_REJECT_REASON_CHOICES, blank=True, null=True)
    marital_status = models.PositiveIntegerField(choices=constant.MARITAS_STATUS_CHOICES,
                                                 default=1)
    job = models.PositiveIntegerField(choices=constant.JOB_CHOICES,
                                      default=1)

    spouse_full_name = models.CharField(max_length=150, blank=True, null=True)
    spouse_id_card_num = models.CharField(max_length=40, blank=True, null=True)
    spouse_birth_date = models.DateField(blank=True, null=True)
    spouse_birth_place = models.CharField(max_length=40, blank=True, null=True)
    mother_name = models.CharField(max_length=150, blank=True, null=True)
    religion = models.CharField(
        max_length=20, choices=constant.RELIGION_CHOICES, blank=True, null=True)
    education = models.CharField(
        max_length=20, choices=constant.EDUCATION_CHOICES, blank=True, null=True)
    ownership_residence = models.CharField(
        max_length=20, choices=constant.RESIDENCE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.owned_by.full_name

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            if self.gender == 1:
                return constant.NO_AVATAR_2_URL
            return constant.NO_AVATAR_1_URL

    def get_avatar_2x(self):
        return self.get_avatar()

    def get_cover(self):
        if self.background_cover:
            return self.background_cover.url
        else:
            return constant.NO_IMAGE_URL

    def get_id_card(self):
        if self.id_card:
            return getattr(self.id_card, 'url')
        else:
            return '-'

    def get_id_card_selfie(self):
        if self.id_card:
            return self.id_card_selfie.url
        else:
            return '-'

    def get_gender(self):
        return dict(constant.GENDER_CHOICES)[self.gender]

    def get_type(self):
        return dict(constant.PROFILE_TYPE_CHOICES)[self.type]

    def get_number(self, *args, **kwargs):
        return str(self.pk).zfill(5)

    def get_age(self, *args, **kwargs):
        today = date.today()
        return today.year - self.birth_date.year

    def get_total_invested(self):
        from core.structures.loan.models import Fund
        total_invested = Fund.objects.filter(
            created_by_id=self.created_by_id,
            status=1
        ).aggregate(
            models.Sum('amount')
        )['amount__sum']
        if total_invested:
            return 'Rp.{:,.0f},-'.format(int(total_invested))
        else:
            return 'Rp.{:,.0f},-'.format(0)

    def get_total_topup(self):
        from enterprise.structures.transaction.models import TopUp
        total_topup = TopUp.objects.filter(
            created_by_id=self.created_by_id,
            status='success'
        ).aggregate(
            models.Sum('amount')
        )['amount__sum']
        if total_topup:
            return 'Rp.{:,.0f},-'.format(int(total_topup))
        else:
            return 'Rp.{:,.0f},-'.format(0)

    def get_cash_balance(self):
        from enterprise.structures.transaction.models import Wallet
        cash_balance = Wallet.objects.filter(
            created_by_id=self.created_by_id
        ).aggregate(
            models.Sum('amount')
        )['amount__sum']
        if cash_balance:
            return 'Rp.{:,.0f},-'.format(int(cash_balance))
        else:
            return 'Rp.{:,.0f},-'.format(0)

    def get_total_withdraw(self):
        from enterprise.structures.transaction.models import Withdraw
        total_withdraw = Withdraw.objects.filter(
            created_by_id=self.created_by_id
        ).aggregate(
            models.Sum('amount')
        )['amount__sum']
        if total_withdraw:
            return 'Rp.{:,.0f},-'.format(int(total_withdraw))
        else:
            return 'Rp.{:,.0f},-'.format(0)

    def get_loan_type(self):
        from core.structures.loan.models import Loan
        loan = Loan.objects.filter(
            created_by_id=self.created_by_id
        ).all()
        if loan:
            return loan


class ProfileDetail(BaseModelGeneric):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Profile Detail')
        verbose_name_plural = _('Profile Details')


class Company(BaseModelGeneric):
    type = models.PositiveIntegerField(choices=constant.COMPANY_TYPE_CHOICES)
    ownership_bussiness = models.PositiveIntegerField(
        choices=constant.COMPANY_OWNERSHIP_CHOICES)
    business_started_date = models.DateField()
    income = models.DecimalField(max_digits=12, decimal_places=2)
    cost_bussiness = models.DecimalField(max_digits=12, decimal_places=2)
    cost_household = models.DecimalField(max_digits=12, decimal_places=2)
    cost_instalments = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    account_number = models.DecimalField(max_digits=20, decimal_places=0)
    total_account_number = models.DecimalField(
        max_digits=12, decimal_places=0)
    total_account_number_other = models.DecimalField(
        max_digits=12, decimal_places=0)
    have_internet_banking = models.BooleanField(default=False)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class ECommerce(BaseModelGeneric):

    type_of_bussiness = models.CharField(
        max_length=20, choices=constant.TYPE_BUSSINESS)
    name_store = models.CharField(max_length=150)
    domain_store = models.CharField(max_length=150)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    transaction_freq = models.DecimalField(max_digits=9, decimal_places=0)
    cashflow = models.DecimalField(max_digits=12, decimal_places=2)
    success_rate = models.DecimalField(max_digits=3, decimal_places=2)
    ecommerce = models.CharField(
        max_length=20, choices=constant.ECOMMERCE)

    class Meta:
        verbose_name = _('ECommerce')
        verbose_name_plural = _('ECommerces')


class CompanyDetail(BaseModelGeneric):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Company Detail')
        verbose_name_plural = _('Company Details')
