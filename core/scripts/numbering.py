'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: numbering.py
# Project: core.bimaasia.id
# File Created: Monday, 2nd September 2019 6:48:14 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Monday, 2nd September 2019 6:48:14 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
from core.structures.loan.models import Loan


def regenerate_numbering():
    Loan.objects.all().update(number='')
    for l in Loan.objects.all():
        l.save()
