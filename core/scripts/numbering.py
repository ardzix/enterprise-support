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
from core.structures.project.models import *


def regenerate_numbering():
    for l in Project.objects.all():
        l.number = ''
        l.save(create_number=False)
    for l in Project.objects.all():
        l.save()
        print(l.get_number())

        for f in l.fund_set.all():
            f.number = ''
            f.save(create_number=False)
        for f in l.fund_set.all():
            f.save()
            print('---%s' % (f.get_number()))
