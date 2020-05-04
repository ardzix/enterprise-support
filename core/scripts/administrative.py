'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: administrative.py
# Project: core.bimaasia.id
# File Created: Tuesday, 18th June 2019 3:25:44 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 18th June 2019 3:25:44 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import csv
import os
from ..structures.account.models import Province, Regency

csv_directory = '%s/scripts/csv' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def import_provices():
    with open('%s/provinces.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            id = row['ID']
            name = row['PROVINCE']
            Province.objects.get_or_create(
                id=id,
                name=name
            )
            line_count += 1
        print(f'Processed {line_count} lines.')

def import_regencies():
    with open('%s/regencies.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            id = row['ID']
            province_id = row['PROVINCE_ID']
            name = row['REGENCY']
            Regency.objects.get_or_create(
                id=id,
                province_id=province_id,
                name=name
            )
            line_count += 1
        print(f'Processed {line_count} lines.')