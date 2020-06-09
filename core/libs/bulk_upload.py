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
import uuid
from slugify import slugify
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from enterprise.structures.common.models import File

from core.libs.email import bulk_upload_report
from core.structures.account.models import (Profile, Address, Phone,
                                            Company, ECommerce, Province, Regency,
                                            District, Kelurahan)
from core.structures.authentication.models import User
from core.structures.loan.models import Loan


def bulk_upload(file, name, uploader):
    print("*** Processing Bul Upload! ***")
    if file.file.name.split('.')[-1] == 'csv':
        import_csv(file, uploader)
    # else:
    #     associate_document(file, name)


def associate_document(file, name):

    try:
        nik, document = name.split('_')
    except:
        raise Exception('Mohon upload dokumen dengan format nama yang benar')

    profile = Profile.objects.filter(id_card_num=nik).last()
    if not profile:
        raise Exception('NIK %s tidak ditemukan' % nik)

    loan = Loan.objects.filter(owned_by=profile.owned_by).last()
    if not loan:
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
    emails = []
    failed = []
    success = []
    for i, line in enumerate(lines):
        if i == 0:
            continue
        _nik = "-"
        try:
            nonce = str(uuid.uuid4())
            row = line.decode('utf-8').replace("\r\n", "")
            cols = row.split(';')
            nik = cols[0].replace("'","")
            cl = len(cols)
            _nik = nik
            # Contact
            email = cols[20] if cols[20] != '' else None
            phone = cols[21].replace("'","") if cols[21] != '' else None

            if email in emails:
                raise Exception('Email %s duplikat')
            emails.append(email)

            # Profile
            full_name = cols[1] if cols[1] != '' else None
            birth_place = cols[2] if cols[2] != '' else None
            birth_date = datetime.datetime.strptime(cols[3], "%d/%m/%Y").date() if cols[3] != '' else None
            gender = cols[4] if cols[4] != '' else None
            marital_status = cols[5] if cols[5] != '' else None
            job = cols[6] if cols[6] != '' else None

            # Address
            id_card_address = cols[7] if cols[7] != '' else None
            id_card_province = cols[8] if cols[8] != '' else None
            id_card_regency = cols[9] if cols[9] != '' else None
            id_card_district = cols[10] if cols[10] != '' else None
            id_card_kelurahan = cols[11] if cols[11] != '' else None
            id_card_postal_code = cols[12] if cols[12] != '' else None
            address = cols[13] if cols[13] != '' else None
            province = cols[14] if cols[14] != '' else None
            regency = cols[15] if cols[15] != '' else None
            district = cols[16] if cols[16] != '' else None
            kelurahan = cols[17] if cols[17] != '' else None
            postal_code = cols[18] if cols[18] != '' else None
            start_live = datetime.datetime.strptime(cols[19], "%d/%m/%Y").date() if cols[19] != '' else None

            # Other info
            spouse_name = cols[22] if cols[22] != '' else None
            spouse_nik = cols[23] if cols[23] != '' else None
            spouse_birth_place = cols[24] if cols[24] != '' else None
            spouse_birth_date = datetime.datetime.strptime(cols[25], "%d/%m/%Y").date() if cols[25] != '' else None
            mother_name = cols[26] if cols[26] != '' else None
            religion = cols[27] if cols[27] != '' else None
            education = cols[28] if cols[28] != '' else None
            ownership_residence = cols[29] if cols[29] != '' else None

            # Business
            business_type = cols[30] if cols[30] != '' else None
            ownership_bussiness = cols[31] if cols[31] != '' else None
            business_started_date = datetime.datetime.strptime(cols[32], "%d/%m/%Y").date() if cols[32] != '' else None
            income = float(cols[33]) if cols[33] != '' else 0
            cost_bussiness = float(cols[34]) if cols[34] != '' else 0
            cost_household = float(cols[35]) if cols[35] != '' else 0
            cost_instalments = float(cols[36]) if cols[36] != '' else 0
            total = float(cost_bussiness + cost_household + cost_instalments)
            account_number = cols[37].replace("'","") if cols[37] != '' else None
            total_account_number = cols[38] if cols[38] != '' else 0
            total_account_number_other = cols[39] if cols[39] != '' else 0
            have_internet_banking = True if cols[40] == 'ya' else False
            current_balance = float(cols[41]) if cols[41] != '' else 0

            # Ecommerce
            type_of_bussiness = cols[42] if cols[42] != '' else 100
            name_store = cols[43] if cols[43] != '' else None
            domain_store = cols[44] if cols[44] != '' else None
            rating = cols[45] if cols[45] != '' else 0
            transaction_freq = cols[46] if cols[46] != '' else 0
            cashflow = cols[47] if cols[47] != '' else 0
            success_rate = cols[48] if cols[48] != '' else 0
            ecommerce = file.owned_by.get_profile().associated_with

            # Loan
            amount = float(cols[49]) if cols[49] != '' else 0
            duration = int(cols[50]) if cols[50] != '' else None

            # Attachment
            ktp = cols[51]
            sku = cols[52]
            selfie = cols[53]
            npwp = cols[54]
            store_picts = []
            for x in range(55, cl):
                store_picts.append(cols[x])

            profile = Profile.objects.filter(id_card_num=nik).last()
            if not profile:
                user = User.objects.filter(email=email).first()
                if not user:
                    user = User.objects.create(
                        full_name=full_name,
                        email=email,
                        is_sent_email=False
                    )
                    Profile.objects.get_or_create(
                        created_by=user,
                    )
            else:
                user = profile.owned_by

            check_loan_exist(user)

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
            profile.nonce = nonce
            profile.save()
            user.full_name = full_name
            user.save()

            # Address
            address_obj = Address.objects.create(
                nonce=nonce,
                created_by=user,
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

            id_address_obj = Address.objects.create(
                nonce=nonce,
                created_by=user,
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

            profile.addresses.set((address_obj, id_address_obj))

            phone, created = Phone.objects.get_or_create(
                number=phone,
                created_by=user
            )
            if created:
                phone.nonce = nonce
                phone.save()
            phone.save()
            profile.phones.add(phone)

            business = Company.objects.create(
                owned_by=profile.owned_by,
                created_by=user,
                nonce=nonce,
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

            ecommerce = ECommerce.objects.create(
                created_by=user,
                nonce=nonce,
                type_of_bussiness=type_of_bussiness,
                name_store=name_store,
                domain_store=domain_store,
                rating=rating,
                transaction_freq=transaction_freq,
                cashflow=cashflow,
                success_rate=success_rate,
                ecommerce=ecommerce
            )

            loan = Loan.objects.create(
                nonce=nonce,
                created_by=user,
                amount=amount,
                duration=duration
            )

            if ktp and ktp != '':
                loan.attachements.add(create_file(ktp, user, 'KTP'))
            if sku and sku != '':
                loan.attachements.add(create_file(sku, user, 'Surat Keterangan Usaha'))
            if selfie and selfie != '':
                loan.attachements.add(create_file(selfie, user, 'Foto Selfie'))
            if npwp and npwp != '':
                loan.attachements.add(create_file(npwp, user, 'NPWP'))
            for sp in store_picts:
                if sp and sp != '':
                    loan.attachements.add(create_file(sp, user, 'Foto Toko'))

            # code bellow is handled in signal
            # loan.bussiness = business
            # loan.ecommerce = ecommerce
            # loan.owned_by = user
            # loan.save()
            loan.publish(uploader)
            success.append(_nik)
        except Exception as e:
            message = str(e)
            if type(e) == IntegrityError:
                message = _('Null value or invalid data type')
            if message == 'unconverted data remains: 7':
                message = 'Format tanggal tidak sesuai'
            failed.append(
                {
                    'nik': _nik,
                    'error': message
                }
            )
            continue
    bulk_upload_report(uploader, success, failed)

def create_file(url, user, name):
    return File.objects.create(
        display_name=name,
        short_name=slugify(name),
        file=url,
        created_by=user
    )


def check_loan_exist(user):
    if Loan.objects.filter(
            owned_by=user,
            status__in=['requested', 'processed', 'approved']).exists():
        raise Exception('Pinjaman telah diajukan sebelumnya')
