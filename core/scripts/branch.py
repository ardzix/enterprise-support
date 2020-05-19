'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: branch.py
# Project: kur.bri.co.id
# File Created: Friday, 8th May 2020 10:14:13 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Friday, 8th May 2020 10:14:13 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2020 PT Bank Rakyat Indonesia, bri.co.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import csv
import os
from ..structures.account.models import Branch, BranchPostalcode

csv_directory = '%s/scripts/csv' % os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


def import_branches():
    with open('%s/branch.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            id = row['BRANCH']
            region = row['REGION']
            number = row['FULL_BRANCH']
            Branch.objects.get_or_create(
                id=id,
                region=region,
                number=number
            )
            line_count += 1
            print(f'Processed {line_count} lines.')

def import_branch_postal_code():
    with open('%s/uker.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            postal_code = row['KODE POS']
            name = row['NAMA UKER']
            line_count += 1
            try:
                BranchPostalcode.objects.get_or_create(
                    postal_code=postal_code,
                    name=name
                )
            except:
                line_count -= 1
            print(f'Processed {line_count} lines.')
