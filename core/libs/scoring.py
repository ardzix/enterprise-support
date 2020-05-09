'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: scoring.py
# Project: kur.bri.co.id
# File Created: Saturday, 9th May 2020 10:11:38 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Saturday, 9th May 2020 10:11:39 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2020 PT Bank Rakyat Indonesia, bri.co.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
from core.structures.loan.models import Loan

class Scoring(object):
    instace = None
    def __init__(self, loan, *args, **kwargs):
        self.instace = loan

    def get_scoring(self):
        pass

    def calculate(self):
        pass

    