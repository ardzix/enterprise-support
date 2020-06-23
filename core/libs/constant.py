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

YES_OR_NO = (
    ('ya', 'Ya'),
    ('tidak', 'Tidak')
)

GENDER_CHOICES = (
    (1, "Pria"),
    (2, "Wanita"),
)

NO_IMAGE_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/NO_IMAGE.png"
NO_AVATAR_1_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/AVATAR_1.png"
NO_AVATAR_2_URL = "https://a75f8eca1cb38315333c-678aa23ddc581c009f308cf5d4dc9c11.ssl.cf6.rackcdn.com/defaults/AVATAR_2.png"
