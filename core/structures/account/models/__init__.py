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
from enterprise.structures.authentication.models import User, EmailVerification
from enterprise.libs import storage

from core.libs import constant

User = settings.AUTH_USER_MODEL


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
    npwp_num = models.CharField(max_length=40, blank=True, null=True)
    id_card_num = models.CharField(max_length=40, blank=True, null=True)
    addresses = models.ManyToManyField(Address, blank=True)
    phones = models.ManyToManyField(Phone, blank=True)
    type = models.PositiveIntegerField(
        choices=constant.PROFILE_TYPE_CHOICES, default=3)
    reject_reason = models.PositiveIntegerField(
        choices=constant.PROFILE_REJECT_REASON_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.owned_by.nick_name

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
            return self.id_card.url
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
        from core.structures.project.models import Fund
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

    def get_project_type(self):
        from core.structures.project.models import Project
        project = Project.objects.filter(
            created_by_id=self.created_by_id
        ).all()
        if project:
            return project


class ProfileDetail(BaseModelGeneric):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Profile Detail')
        verbose_name_plural = _('Profile Details')


class CompanySector(BaseModelGeneric):
    display_name = models.CharField(max_length=300)
    short_name = models.SlugField(max_length=300)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Company Sector')
        verbose_name_plural = _('Company Sectors')


class Company(BaseModelGeneric):
    display_name = models.CharField(max_length=300)
    short_name = models.SlugField(max_length=300)
    phone = models.CharField(max_length=100)
    staffs = models.ManyToManyField(User, blank=True)

    registration_number = models.CharField(max_length=100)
    type = models.PositiveIntegerField(choices=constant.COMPANY_TYPE_CHOICES)
    country = models.CharField(
        max_length=3,
        choices=constant.COUNTRY_CHOICES,
        default='IDN')
    year_built = models.PositiveIntegerField()
    sector = models.ForeignKey(CompanySector, on_delete=models.CASCADE)

    logo = models.ImageField(
        storage=storage.LOGO_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    cover = models.ImageField(
        storage=storage.COVER_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.display_name

    def is_executive(self, user):
        return self.executive.pk == user.pk

    def is_staff(self, user):
        return user.id in self.staffs.values_list('id', flat=True)

    def get_short_description(self):
        return '%s . . .' % self.description[0:150]

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return None

    def get_type(self):
        return dict(constant.COMPANY_TYPE_CHOICES)[self.type]

    def get_cover(self):
        if self.cover:
            return self.cover.url
        else:
            return NO_IMAGE_URL

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class CompanyDetail(BaseModelGeneric):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Company Detail')
        verbose_name_plural = _('Company Details')
