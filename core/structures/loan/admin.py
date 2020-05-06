'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: admin.py
# Project: core.bimaasia.id
# File Created: Wednesday, 24th April 2019 11:13:35 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 24th April 2019 11:13:35 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.contrib import admin
from .models import *


class GradeAdmin(admin.ModelAdmin):
    pass


class LoanTypeAdmin(admin.ModelAdmin):
    pass


class DocumentKeyAdmin(admin.ModelAdmin):
    pass


class LoanAdmin(admin.ModelAdmin):
    pass


class FundAdmin(admin.ModelAdmin):
    pass


admin.site.register(Grade, GradeAdmin)
admin.site.register(LoanType, LoanTypeAdmin)
admin.site.register(DocumentKey, DocumentKeyAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(Loan, LoanAdmin)
