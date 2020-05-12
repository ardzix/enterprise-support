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
from ..structures.account.models import Province, Regency, District, Kelurahan

csv_directory = '%s/scripts/csv' % os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clear_all():
    Province.objects.all().delete()

def import_provices():
    with open('%s/state_baru.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            id = row['state_code']
            name = row['state']
            Province.objects.get_or_create(
                id=id,
                name=name
            )
            line_count += 1
            print(f'Processed {line_count} line stae.')

def import_regencies():
    with open('%s/city_baru.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            id = row['city_code']
            province_id = row['state_code']
            name = row['city']
            Regency.objects.get_or_create(
                id=id,
                province_id=province_id,
                name=name
            )
            line_count += 1
            print(f'Processed {line_count} line regency.')

def import_districts():
    with open('%s/kecamatan_baru.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            regency_id = row['city_code']
            name = row['kecamatan']
            District.objects.get_or_create(
                regency_id=regency_id,
                name=name
            )
            line_count += 1
            print(f'Processed {line_count} line district.')

def import_kelurahan():
    with open('%s/kelurahan_baru.csv' % csv_directory, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        districts = {}
        for row in csv_reader:
            district_id = districts.get(row['kecamatan'])
            if not district_id:
                try:
                    d = District.objects.get(name=row['kecamatan'], regency_id=row['city_code'])
                except:
                    d = District.objects.filter(name=row['kecamatan']).last()
                    if not d:
                        continue
                districts[d.name] = d.id
            district_id = districts.get(row['kecamatan'])
            name = row['kelurahan']
            postal_code = row['kode_pos']
            Kelurahan.objects.get_or_create(
                district_id=district_id,
                name=name,
                postal_code=postal_code
            )
            line_count += 1
            print(f'Processed {line_count} line kelurahan.')