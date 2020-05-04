'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: admin.py
# Project: core.bimaasia.id
# File Created: Monday, 22nd April 2019 11:28:06 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Monday, 22nd April 2019 11:28:06 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.contrib import admin
from .models import *


class GuaranteeAdmin(admin.ModelAdmin):
    pass


class GuaranteeDetailAdmin(admin.ModelAdmin):
    pass


class FinancialAdmin(admin.ModelAdmin):
    pass


class SocialMediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guarantee, GuaranteeAdmin)
admin.site.register(GuaranteeDetail, GuaranteeDetailAdmin)
admin.site.register(Financial, FinancialAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
