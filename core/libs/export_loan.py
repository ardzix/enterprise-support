from core.libs.generate_csv import generate_csv
from .email import send_email_loan_report
import time

CSV_HEADERS_LOAN = ["NIK", "Nama Lengkap", "Tempat Lahir", "Tanggal Lahir",
                    "Jenis Kelamin", "Status pernikahan", "Pekerjaan", "Alamat Lengkap KTP",
                    "Propinsi KTP", "Kota/Kabupaten KTP", "Kecamatan KTP", "Kelurahan KTP",
                    "Kode Pos KTP", "Alamat Lengkap Domisili", "Propinsi Domisili",
                    "Kota/Kabupaten Domisili", "Kecamatan Domisili", "Kelurahan Domisili",
                    "Kode Pos Domisili", "Tanggal Mulai Tinggal", "Email", "Telepon",
                    "Nama Pasangan", "NIK Pasangan", "Tempat Lahir Pasangan",
                    "Tanggal Lahir Pasangan", "Nama Ibu Kandung", "Agama", "Pendidikan",
                    "Kepemilikan Rumah Tinggal", "Jenis Usaha", "Kepemilikan Usaha",
                    "Tanggal Mulai Usaha", "Penghasilan Per Bulan", "Biaya Usaha",
                    "Biaya Rumah Tangga", "Biaya Cicilan", "No Rekening BRI",
                    "Jumlah Rekening BRI", "Jumlah Rekening Bank Lain",
                    "Memiliki Internet Banking", "Saldo Simpanan Bulan Ini",
                    "Jenis Usaha Ecommerce", "Nama Toko di Ecommerce",
                    "Domain Toko di Ecommerce", "Nama Ecommerce", "Rating Toko", "Frekuensi Transaki 6 bulan terakhir",
                    "Cashflow 6 bulan Terakhir", "Sukses Rate Transaksi",
                    "Plafon Pengajuan", "Plafon Disetujui", "Jangka Waktu", "Jangka Waktu Disetujui",
                    "Tanggal Pencairan",
                    "Grade", "Score", "Status Pinjaman", "Alasan Ditolak",
                    "Tanngal Pengajuan", "Tanngal Diproses", "Tanngal Disetujui", "Tanngal Ditolak"]

CSV_FILE_HEADERS = ["URL KTP", "URL Surat Keterangan Usaha",
                    "URL Foto Selfie", "URL NPWP", "URL Foto Usaha"]


def export_loan(loans, user_email, suffix='', additional_data=[]):
    start = time.time()
    data = []

    loans = loans.select_related(
        'owned_by', 'bussiness', 'ecommerce'
    ).prefetch_related('attachements')

    for _loan in loans:
        profile = _loan.owned_by.get_profile()
        company = _loan.bussiness
        ecommerce = _loan.ecommerce
        attachments = _loan.attachements.all()

        if profile:
            province_ktp, regency_ktp, \
                district_ktp, kelurahan_ktp, address_ktp, \
                postal_code_ktp, \
                start_live_ktp = profile.get_detail_address(name="KTP")

            province_domisili, regency_domisili, \
                district_domisili, kelurahan_domisili, address_domisili, \
                postal_code_domisili, \
                start_live_domisili = profile.get_detail_address(
                    name="Domisili")

            nik = profile.id_card_num
            full_name = profile.owned_by.full_name
            birth_place = profile.birth_place if profile.birth_place else ""
            birth_date = profile.birth_date if profile.birth_date else ""
            gender = profile.get_gender_display()
            marital_status = profile.get_marital_status_display()
            job = profile.get_job_display()
            address_ktp = address_ktp.replace(",", ".")
            province_ktp = province_ktp
            regency_ktp = regency_ktp
            district_ktp = district_ktp
            kelurahan_ktp = kelurahan_ktp
            postal_code_ktp = postal_code_ktp
            address_domisili = address_domisili.replace(",", ".")
            province_domisili = province_domisili
            regency_domisili = regency_domisili
            district_domisili = district_domisili
            kelurahan_domisili = kelurahan_domisili
            postal_code_domisili = postal_code_domisili
            start_live_from = start_live_domisili
            email = profile.owned_by.email
            phone_number = profile.get_phone() if profile.phones.exists() else ""
            spouse_full_name = profile.spouse_full_name if profile.spouse_full_name else ""
            nik_spouse = profile.spouse_id_card_num if profile.spouse_id_card_num else ""
            spouse_birth_place = profile.spouse_birth_place if profile.spouse_birth_place else ""
            spouse_birth_date = profile.spouse_birth_place if profile.spouse_birth_place else ""
            mother_name = profile.mother_name if profile.mother_name else ""
            religion = profile.get_religion_display() if profile.religion else ""
            education = profile.get_education_display() if profile.education else ""
            ownership_residence = profile.get_ownership_residence_display(
            ) if profile.ownership_residence else ""

            # company
            business_type = company.get_type_display() if company else ""
            business_ownership = company.get_ownership_bussiness_display() if company else ""
            business_started_date = company.business_started_date.strftime(
                "%d-%m-%Y") if company else ""
            business_income = company.income if company else ""
            business_cost = company.cost_bussiness if company else ""
            cost_household = company.cost_household if company else ""
            cost_instalments = company.cost_instalments if company else ""
            account_number = company.account_number if company else ""
            total_account_number = company.total_account_number if company else ""
            total_account_number_other = company.total_account_number_other if company else ""
            have_internet_banking = company.have_internet_banking if company else ""
            current_balance = company.current_balance if company else ""

            # ecommerce
            ecom_type_of_bussiness = ecommerce.get_type_of_bussiness_display() if ecommerce else ""
            ecom_store_name = ecommerce.name_store if ecommerce else ""
            ecom_domain = ecommerce.domain_store if ecommerce else ""
            ecom_name = ecommerce.ecommerce if ecommerce else ""
            ecom_rating = ecommerce.rating if ecommerce else ""
            ecom_transaction_freq = ecommerce.transaction_freq if ecommerce else ""
            ecom_cashflow = ecommerce.cashflow if ecommerce else ""
            ecom_success_rate = ecommerce.get_success_rate() if ecommerce else ""
            loan_amount = _loan.amount
            loan_approved_amount = _loan.approved_amount
            loan_duration = _loan.duration
            loan_approved_duration = _loan.approved_duration
            loan_disbursement_date = _loan.disbursement_date
            loan_grade = _loan.get_grade()
            loan_score = _loan.score
            loan_status = _loan.status
            loan_notes = _loan.notes
            loan_account_number = _loan.account_number

            loan_created_at = _loan.created_at
            loan_processed_at = _loan.processed_at
            loan_approved_at = _loan.approved_at
            loan_rejected_at = _loan.rejected_at

            ktp = attachments.filter(short_name='ktp').first()
            url_ktp = ktp.get_safe_url() if ktp else ""
            k_u = attachments.filter(
                short_name='surat-keterangan-usaha').first()
            url_k_u = k_u.get_safe_url() if k_u else ""
            selfie = attachments.filter(short_name='foto-selfie').first()
            url_selfie = selfie.get_safe_url() if selfie else ""
            npwp = attachments.filter(short_name='npwp').first()
            url_npwp = npwp.get_safe_url() if npwp else ""
            row = [
                nik, full_name, birth_place, birth_date, gender,
                marital_status, job, address_ktp, province_ktp, regency_ktp,
                district_ktp, kelurahan_ktp, postal_code_ktp,
                address_domisili, province_domisili, regency_domisili,
                district_domisili, kelurahan_domisili,
                postal_code_domisili, start_live_from, email,
                phone_number, spouse_full_name, nik_spouse,
                spouse_birth_place, spouse_birth_date,
                mother_name, religion, education, ownership_residence,
                business_type, business_ownership, business_started_date,
                business_income, business_cost, cost_household,
                cost_instalments, account_number, total_account_number,
                total_account_number_other, have_internet_banking,
                current_balance, ecom_type_of_bussiness, ecom_store_name,
                ecom_domain, ecom_name, ecom_rating, ecom_transaction_freq,
                ecom_cashflow, ecom_success_rate,
                loan_amount, loan_approved_amount, loan_duration, loan_approved_duration,
                loan_disbursement_date,
                loan_grade, loan_score, loan_status, loan_notes,
                loan_created_at, loan_processed_at, loan_approved_at, loan_rejected_at]

            for ad in additional_data:
                if ad == 'loan_account_number':
                    row.append(loan_account_number)

            row += [url_ktp, url_k_u, url_selfie, url_npwp]
            for f in attachments.exclude(short_name__in=[
                'ktp', 'surat-keterangan-usaha', 'foto-selfie', 'npwp'
            ]):
                row.append(f.get_safe_url())

            data.append(row)
    headers = CSV_HEADERS_LOAN
    for ad in additional_data:
        if ad == 'loan_account_number':
            headers.append('Rekening Pinjaman')
    headers += CSV_FILE_HEADERS
    end = time.time()
    print('Finished in {}s'.format(end-start))

    filename, data, content_type = generate_csv(
        data, "loan_report%s" % suffix, headers, send_email=True)

    return send_email_loan_report(data, filename, content_type, user_email)
