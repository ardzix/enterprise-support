'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: agreement.py
# Project: core.bimaasia.id
# File Created: Tuesday, 30th July 2019 5:50:30 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 30th July 2019 5:50:30 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

from core.structures.account.models import Company
from core.structures.project.models import Project, MasterAgreement, ParticipationAgreement
from enterprise.structures.transaction.models import BankAccount

def generate_ma(project):
    ma = project.masteragreement_set.first()
    if not ma:
        borrower = project.owned_by
        company = Company.objects.filter(owned_by=borrower).last()
        address = None
        if company:
            address = company.address
        if not address:
            address = borrower.get_profile().addresses.first()
        ma = MasterAgreement.objects.create(
            project = project,
            created_by = borrower,
            company = company,
            address = address
        )
    return ma

def generate_pa(fund):
    if not fund.participationagreement_set.first():
        project = fund.project
        ma = project.masteragreement_set.last()
        lender = fund.owned_by
        bank_account = BankAccount.objects.filter(owned_by=lender).last()
        ParticipationAgreement.objects.create(
            ma = ma,
            fund = fund,
            created_by = lender,
            address = lender.get_profile().addresses.first(),
            bank_account = bank_account,
        )