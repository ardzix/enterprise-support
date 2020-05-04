'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: core.bimaasia.id
# File Created: Monday, 22nd April 2019 11:28:20 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Monday, 22nd April 2019 11:28:20 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.db import models
from django.utils.text import slugify
from django.contrib.gis.db import models as geo
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from enterprise.structures.common.models import File
from enterprise.structures.common.models.base import BaseModelGeneric, BaseModelUnique
from enterprise.libs import storage

from core.libs import constant


User = settings.AUTH_USER_MODEL


class Guarantee(BaseModelGeneric):
    type = models.PositiveIntegerField(choices=constant.GUARANTEE_TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Guarantee')
        verbose_name_plural = _('Guarantees')


class GuaranteeDetail(BaseModelGeneric):
    guarantee = models.ForeignKey(Guarantee, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Guarantee Detail')
        verbose_name_plural = _('Guarantee Details')


class Financial(BaseModelGeneric):
    currency = models.CharField(
        choices=constant.CURRENCY_CHOICES,
        default='IDR',
        max_length=3)
    monthly_income = models.DecimalField(max_digits=19, decimal_places=2)
    year_income = models.DecimalField(max_digits=19, decimal_places=2)
    year_bruto_income = models.DecimalField(max_digits=19, decimal_places=2)
    year_net_income = models.DecimalField(max_digits=19, decimal_places=2)
    total_asset = models.PositiveIntegerField()
    total_obligation = models.PositiveIntegerField()
    have_other_loan = models.BooleanField(default=False)
    have_ligitation = models.BooleanField(default=False)

    def __str__(self):
        return self.owned_by

    class Meta:
        verbose_name = _('Financial')
        verbose_name_plural = _('Financials')


class SocialMedia(BaseModelGeneric):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Medias')