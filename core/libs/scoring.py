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
import datetime
from core.structures.account.models import Branch, Profile


class Scoring(object):
    instance = None
    score = 0
    profile = None

    def __init__(self, loan, score=500, *args, **kwargs):
        self.instance = loan
        self.score = score
        self.profile = Profile.objects.filter(owned_by=self.instance.owned_by).last()
        if not self.profile:
            self.profile = Profile.objects.filter(nonce=self.instance.nonce).last()
        self.calculate()

    def get_score(self):
        return self.score

    def calculate(self):
        self.calculate_duration()
        self.calculate_plafond()
        self.calculate_region()
        self.calculate_work_duration()
        self.calculate_domicile_duration()
        self.calculate_net_profit()
        self.calculate_residence_ownership()
        self.calculate_marital_status()
        self.calculate_age()
        self.calculate_activa()
        self.calculate_total_account()
        self.calculate_internet_banking()

    def calculate_duration(self):
        duration = self.instance.duration
        if duration < 24:
            self.score -= 81
        elif 24 <= duration < 36:
            self.score += 11
        else:
            self.score += 20

    def calculate_plafond(self):
        plafond = self.instance.amount
        if plafond < 8000000:
            self.score -= 25
        elif 8 <= plafond < 20:
            self.score -= 5
        elif 20 <= plafond < 25:
            self.score += 5
        else:
            self.score += 8

    def calculate_region(self):
        account = self.instance.bussiness.account_number
        try:
            branch = Branch.objects.get(number=str(account)[0:4])
        except:
            self.score -= 19
            return None
        region = branch.region
        if region == 'I' or region == 'J' or region == 'K' or region == 'L':
            self.score += 13
        elif region == 'M':
            self.score += 27
        else:
            self.score -= 19

    def calculate_work_duration(self):
        end = self.instance.created_at.date().year
        start = self.instance.bussiness.business_started_date.year
        delta = end - start
        if delta < 3:
            self.score -= 18
        elif 3 <= delta < 5:
            self.score -= 9
        elif 5 <= delta < 9:
            self.score += 3
        else:
            self.score += 13

    def calculate_domicile_duration(self):
        address = self.profile.addresses.filter(name='Domisili').last()
        if address and address.start_live:
            duration = datetime.date.today().year - address.start_live.year
            if duration < 7:
                self.score -= 15
            elif 7 <= duration < 16:
                self.score -= 1
            elif 16 <= duration < 28:
                self.score += 3
            else:
                self.score += 13

    def calculate_net_profit(self):
        net_profit = self.instance.bussiness.income - self.instance.bussiness.total
        if net_profit < 700000:
            self.score -= 14
        elif 700000 <= net_profit < 1100000:
            self.score += 1
        elif 1100000 <= net_profit < 3400000:
            self.score += 6
        else:
            self.score += 22

    def calculate_residence_ownership(self):
        ownership = self.profile.ownership_residence
        if ownership == 'milik-sendiri':
            self.score += 6
        elif ownership == 'milik-orang-tua':
            self.score -= 13
        else:
            self.score -= 28

    def calculate_marital_status(self):
        marital_status = self.profile.marital_status
        if marital_status == 1:
            self.score += 7
        elif marital_status == 2:
            self.score -= 24
        else:
            self.score -= 30

    def calculate_age(self):
        age = datetime.date.today().year - self.profile.birth_date.year
        if age < 26:
            self.score -= 15
        elif 26 <= age < 30:
            self.score -= 7
        elif 30 <= age < 34:
            self.score -= 3
        elif 34 <= age < 44:
            self.score += 2
        else:
            self.score += 5

    def calculate_activa(self):
        activa = self.instance.bussiness.current_balance
        if activa < 500000:
            self.score -= 30
        elif 500000 <= activa < 4500000:
            self.score -= 3
        elif 4500000 <= activa < 9000000:
            self.score += 15
        elif 9000000 <= activa < 14500000:
            self.score += 31
        else:
            self.score += 57

    def calculate_total_account(self):
        total = self.instance.bussiness.total_account_number + \
            self.instance.bussiness.total_account_number_other
        if total < 2:
            self.score += 4
        elif 2 <= total < 3:
            self.score -= 7
        else:
            self.score -= 14

    def calculate_internet_banking(self):
        if self.instance.bussiness.have_internet_banking:
            self.score += 17
        else:
            self.score -= 2


def pre_screen(loan):
    '''
    Calculate pre screen scoring
    Params: Loan object
    Returns: Is Approved, Grade Reduction
    '''
    rating = loan.ecommerce.rating
    transaction_freq = loan.ecommerce.transaction_freq
    success_rate = loan.ecommerce.success_rate
    continue_score = 0
    considered_score = 0
    rejected_score = 0

    if rating > 3.5:
        continue_score += 1
    elif 2.43 <= rating <= 3.5:
        considered_score += 1
    else:
        rejected_score += 1

    if transaction_freq > 7043:
        continue_score += 1
    elif 1350 <= transaction_freq <= 7043:
        considered_score += 1
    else:
        rejected_score += 1

    if success_rate > 0.81 and continue_score == 2:
        continue_score += 1
    elif continue_score < 2 and success_rate >= 0.85:
        considered_score += 1
    else:
        rejected_score += 1

    # Return: approved, minus grade
    if continue_score == 3:
        return True, 0
    elif continue_score == 2:
         return True, -1
    elif considered_score >=2 and continue_score>=1:
         return True, -2
    else: 
        return False, 0
