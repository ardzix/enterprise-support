'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: agrement.py
# Project: core.bimaasia.id
# File Created: Tuesday, 30th July 2019 5:19:01 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 30th July 2019 5:19:18 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

from core.structures.project.models import Project
from ..libs.agreement import generate_ma, generate_pa


def generate_agreement_data():
    for project in Project.objects.all():
        generate_ma(project)
        for fund in project.fund_set.all():
            generate_pa(fund)
