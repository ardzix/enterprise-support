'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: constants.py
# Project: core.ayopeduli.id
# File Created: Wednesday, 31st October 2018 7:32:35 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 31st October 2018 7:32:35 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import pycountry

COUNTRY_CHOICES = [(country.alpha_3, country.name)
                   for country in list(pycountry.countries)]
COUNTRY_KEYS = [country.alpha_3 for country in list(pycountry.countries)]
CURRENCY_CHOICES = [(currency.alpha_3, currency.name)
                    for currency in list(pycountry.currencies)]
LANGUAGE_CHOICES = [(language.alpha_3, language.name)
                    for language in list(pycountry.languages)]

GENDER_CHOICES = (
    (1, _('Male')),
    (2, _('Female')),
)

LOAN_INTEREST_CHOICES = (
    (Decimal('0.03'), '3%'),
    (Decimal('0.035'), '3.5%'),
    (Decimal('0.04'), '4%'),
    (Decimal('0.045'), '4.5%'),
    (Decimal('0.05'), '5%'),
)

LOAN_DURATION_CHOICES = (
    (1, _('1 Month')),
    (2, _('2 Months')),
    (3, _('3 Months')),
    (4, _('4 Months')),
    (5, _('5 Months')),
    (6, _('6 Months')),
    (7, _('7 Months')),
    (8, _('8 Months')),
    (9, _('9 Months')),
    (10, _('10 Months')),
    (11, _('11 Months')),
    (12, _('12 Months')),
    (13, _('13 Months')),
    (14, _('14 Months')),
    (15, _('15 Months')),
    (16, _('16 Months')),
    (17, _('17 Months')),
    (18, _('18 Months')),
    (19, _('19 Months')),
    (20, _('20 Months')),
    (21, _('21 Months')),
    (22, _('22 Months')),
    (23, _('23 Months')),
    (24, _('24 Months')),
)

ADMIN_FEE_CHOICES = (
    (Decimal('0.01'), '1%'),
    (Decimal('0.02'), '2%'),
    (Decimal('0.03'), '3%'),
    (Decimal('0.04'), '4%'),
    (Decimal('0.05'), '5%'),
    (Decimal('0.06'), '6%'),
    (Decimal('0.07'), '7%'),
    (Decimal('0.08'), '8%'),
    (Decimal('0.09'), '9%'),
    (Decimal('0.1'), '10%')
)

PROJECT_STATUS_CHOICES = (
    ('requested', _('Requested')),
    ('processed', _('Processed')),
    ('crm_approved', _('CRM Approved')),
    ('crm_rejected', _('CRM Rejected')),
    ('approved', _('Approved')),
    ('rejected', _('Rejected')),
    ('published', _('Published')),
    ('unpublished', _('UnPublished')),
    ('processed', _('Processed')),
    ('disbursed', _('Disbursed')),
    ('closed', _('Closed')),
)

PAYMENT_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('paid', _('Paid')),
    ('expired', _('Expired')),
    ('cancelled', _('Cancelled')),
)

GUARANTEE_TYPE_CHOICES = (
    (1, _('Car')),
    (2, _('Motorcycle')),
    (3, _('Inventory')),
    (4, _('Account Receivable/Invoice')),
    (5, _('Gold/Jewelry')),
    (6, _('Insurance')),
    (99, _('Others')),
)

COMPANY_TYPE_CHOICES = (
    (1, 'PT'),
    (2, 'CV'),
    (3, 'UKM'),
)

LOAN_TYPE_CHOICES = (
    (1, _('Student Loan')),
    (2, _('Business')),
)

PROFILE_TYPE_CHOICES = (
    (1, _('Borrower')),
    (2, _('Lender')),
    (3, _('Undefined'))
)

PROFILE_REJECT_REASON_CHOICES = (
    (1, _('ID Card can not be read')),
    (2, _('Bank account verification failed')),
    (3, _('Bank account verification failed')),
)

LOAN_AMOUNT_CHOICES = (
    (50000000, 'RP.50.000.000,-'),
    (100000000, 'RP.100.000.000,-'),
    (150000000, 'RP.150.000.000,-'),
    (200000000, 'RP.200.000.000,-'),
    (250000000, 'RP.250.000.000,-'),
    (300000000, 'RP.300.000.000,-'),
    (350000000, 'RP.350.000.000,-'),
    (400000000, 'RP.400.000.000,-'),
    (450000000, 'RP.450.000.000,-'),
    (500000000, 'RP.500.000.000,-'),
    (550000000, 'RP.550.000.000,-'),
    (600000000, 'RP.600.000.000,-'),
    (650000000, 'RP.650.000.000,-'),
    (700000000, 'RP.700.000.000,-'),
    (750000000, 'RP.750.000.000,-'),
    (800000000, 'RP.800.000.000,-'),
    (850000000, 'RP.850.000.000,-'),
    (900000000, 'RP.900.000.000,-'),
    (950000000, 'RP.950.000.000,-'),
    (1000000000, 'RP.1.000.000.000,-'),
    (1250000000, 'RP.1.250.000.000,-'),
    (1500000000, 'RP.1.500.000.000,-'),
    (1750000000, 'RP.1.750.000.000,-'),
    (2000000000, 'RP.2.000.000.000,-'),
)

FINANCIAL_DATATYPE_CHOICES = (
    (1, _('Fiscal')),
    (2, _('Score')),
    (3, _('Weight')),
    (4, _('Fiscal & Score')),
    (5, _('Weight & Score')),
)

ARP_ANALYSIS_CHOICES = (
    (1, _('Account Receivable')),
    (2, _('Account Payable')),
)

NO_IMAGE_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/NO_IMAGE.png"
NO_AVATAR_1_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/AVATAR_1.png"
NO_AVATAR_2_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/AVATAR_2.png"
