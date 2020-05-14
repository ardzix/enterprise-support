'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: bulk_upload.py
# Project: kur.bri.co.id
# File Created: Wednesday, 13th May 2020 12:38:42 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Wednesday, 13th May 2020 12:38:43 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2020 PT Bank Rakyat Indonesia, bri.co.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import datetime
import urllib
from slugify import slugify
from core.structures.account.models import (Profile, Address, Phone,
                                            Company, ECommerce, Province, Regency,
                                            District, Kelurahan)
from core.structures.authentication.models import User
from core.structures.loan.models import Loan


def bulk_upload(file, name, uploader):
    if file.file.name.split('.')[-1] == 'csv':
        import_csv(file, uploader)
    else:
        associate_document(file, name)


def associate_document(file, name):
    nonce = file.nonce
    loans = Loan.objects.filter(nonce=nonce)
    if not loans:
        raise Exception('Mohon upload dokumen CSV terlebih dahulu')
    try:
        nik, document = name.split('_')
    except:
        raise Exception('Mohon upload dokumen dengan format nama yang benar')

    profile = Profile.objects.filter(id_card_num=nik).last()
    if not profile:
        raise Exception('NIK %s tidak ditemukan' % nik)
    try:
        loan = loans.get(owned_by=profile.owned_by)
    except:
        raise Exception('Data pinjaman tidak ditemukan')
    file.display_name = document
    file.short_name = slugify(document)
    file.save()
    loan.attachements.add(file)

def import_csv(file, uploader):
    try:
        lines = file.file.readlines()
    except:
        u = urllib.request.urlopen(file.file.url)
        lines = u.readlines()
    for i, line in enumerate(lines):
        if i == 0:
            continue
        row = line.decode('utf-8')
        cols = row.split(',')

        # Profile
        nik = cols[0]
        full_name = cols[1]
        birth_place = cols[2]
        birth_date = datetime.datetime.strptime(cols[3], "%d/%m/%Y").date()
        gender = cols[4]
        marital_status = cols[5]
        job = cols[6]

        # Address
        id_card_address = cols[7]
        id_card_province = cols[8]
        id_card_regency = cols[9]
        id_card_district = cols[10]
        id_card_kelurahan = cols[11]
        id_card_postal_code = cols[12]
        address = cols[13]
        province = cols[14]
        regency = cols[15]
        district = cols[16]
        kelurahan = cols[17]
        postal_code = cols[18]
        start_live = datetime.datetime.strptime(cols[19], "%d/%m/%Y").date()

        # Contact
        email = cols[20]
        phone = cols[21]

        # Other info
        spouse_name = cols[22]
        spouse_nik = cols[23]
        spouse_birth_place = cols[24]
        spouse_birth_date = datetime.datetime.strptime(cols[25], "%d/%m/%Y").date()
        mother_name = cols[26]
        religion = cols[27]
        education = cols[28]
        ownership_residence = cols[29]

        # Business
        business_type = cols[30]
        ownership_bussiness = cols[31]
        business_started_date = datetime.datetime.strptime(cols[32], "%d/%m/%Y").date()
        income = float(cols[33])
        cost_bussiness = float(cols[34])
        cost_household = float(cols[35])
        cost_instalments = float(cols[36])
        total = float(cost_bussiness + cost_household + cost_instalments)
        account_number = cols[37]
        total_account_number = cols[38]
        total_account_number_other = cols[39]
        have_internet_banking = True if cols[40] == 'ya' else False
        current_balance = float(cols[41])

        # Ecommerce
        type_of_bussiness = cols[42]
        name_store = cols[43]
        domain_store = cols[44]
        rating = cols[45]
        transaction_freq = cols[46]
        cashflow = cols[47]
        success_rate = cols[48]
        ecommerce = file.owned_by.get_profile().associated_with

        # Loan
        amount = float(cols[49])
        duration = int(cols[50])

        profile = Profile.objects.filter(id_card_num=nik).last()
        if not profile:
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create(
                    full_name=full_name,
                    email=email
                )
            try:
                profile, created = Profile.objects.get_or_create(
                    created_by=user,
                )
            except:
                profile = Profile.objects.filter(created_by=user).last()
        else:
            user = profile.owned_by

        profile = Profile.objects.filter(owned_by=user).last()
        profile.id_card_num = nik
        profile.birth_place = birth_place
        profile.birth_date = birth_date
        profile.gender = gender
        profile.marital_status = marital_status
        profile.job = job
        profile.spouse_full_name = spouse_name
        profile.spouse_id_card_num = spouse_nik
        profile.spouse_birth_place = spouse_birth_place
        profile.spouse_birth_date = spouse_birth_date
        profile.mother_name = mother_name
        profile.religion = religion
        profile.education = education
        profile.ownership_residence = ownership_residence
        profile.nonce = file.nonce
        profile.save()
        user.full_name = full_name
        user.save()

        # Address
        address_obj = Address.objects.create(
            nonce=file.nonce,
            created_by=uploader,
            owned_by=user,
            name="Domisili",
            address=address,
            province=Province.objects.filter(
                name__icontains=province).last(),
            regency=Regency.objects.filter(name__icontains=regency).last(),
            district=District.objects.filter(
                name__icontains=district).last(),
            kelurahan=Kelurahan.objects.filter(
                name__icontains=kelurahan).last(),
            postal_code=postal_code,
            start_live=start_live
        )
        address_obj.owned_by = profile.owned_by
        address_obj.save()

        id_address_obj = Address.objects.create(
            nonce=file.nonce,
            created_by=uploader,
            owned_by=user,
            name="KTP",
            address=id_card_address,
            province=Province.objects.filter(
                name__icontains=id_card_province).last(),
            regency=Regency.objects.filter(
                name__icontains=id_card_regency).last(),
            district=District.objects.filter(
                name__icontains=id_card_district).last(),
            kelurahan=Kelurahan.objects.filter(
                name__icontains=id_card_kelurahan).last(),
            postal_code=id_card_postal_code
        )
        id_address_obj.owned_by = profile.owned_by
        id_address_obj.save()

        profile.addresses.set((address_obj, id_address_obj))

        phone, created = Phone.objects.get_or_create(
            number=phone,
            created_by=file.owned_by
        )
        if created:
            phone.nonce = file.nonce
            phone.save()
        phone.save()
        profile.phones.add(phone)

        business = Company.objects.create(
            owned_by=profile.owned_by,
            created_by=uploader,
            nonce=file.nonce,
            type=business_type,
            ownership_bussiness=ownership_bussiness,
            business_started_date=business_started_date,
            income=income,
            cost_bussiness=cost_bussiness,
            cost_household=cost_household,
            cost_instalments=cost_instalments,
            total=total,
            account_number=account_number,
            total_account_number=total_account_number,
            total_account_number_other=total_account_number_other,
            have_internet_banking=have_internet_banking,
            current_balance=current_balance
        )
        business.owned_by = profile.owned_by
        business.save()

        ecommerce = ECommerce.objects.create(
            created_by=uploader,
            nonce=file.nonce,
            type_of_bussiness=type_of_bussiness,
            name_store=name_store,
            domain_store=domain_store,
            rating=rating,
            transaction_freq=transaction_freq,
            cashflow=cashflow,
            success_rate=success_rate,
            ecommerce=ecommerce
        )
        ecommerce.owned_by = profile.owned_by
        ecommerce.save()

        loan = Loan.objects.create(
            nonce=file.nonce,
            created_by=uploader,
            amount=amount,
            duration=duration
        )
        loan.bussiness = business
        loan.ecommerce = ecommerce
        loan.owned_by = profile.owned_by
        loan.save()
