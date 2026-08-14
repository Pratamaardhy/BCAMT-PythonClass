print("=== LOAN ELIGIBILITY CHECKER ===")

# system params (Diperbaiki menjadi dictionary menggunakan {})
THRESHOLD = {
    "min_monthly_income": 5_000_000,
    "max_loan_amount": 50_000_000,
    "min_tenor": 6,
    "max_tenor": 36,
    "eligible_employment": "permanent"
}

# TODO: wrap dengan error handling
try:
    name = input("Customer Name: ")

    # TODO: input monthly income
    monthly_income = float(input("Monthly Income (Rp): "))

    # TODO: input loan amount
    loan_amount = float(input("Loan Amount (Rp): "))

    # TODO: input tenor
    tenor = int(input("Tenor (months): "))

    # TODO: input employment status
    employment_status = input("Employment Status (e.g., permanent, contract, freelance): ").strip().lower()

    # TODO: hitung cicilan
    # (Asumsi perhitungan dasar tanpa bunga, cukup pokok pinjaman / tenor)
    monthly_installment = loan_amount / tenor

    # TODO: tentukan apakah customer eligible & kumpulkan alasan penolakan
    rejection_reasons = []

    if monthly_income < THRESHOLD["min_monthly_income"]:
        rejection_reasons.append(f"Pendapatan bulanan di bawah minimum (Rp {THRESHOLD['min_monthly_income']:,})")
        
    if loan_amount > THRESHOLD["max_loan_amount"]:
        rejection_reasons.append(f"Jumlah pinjaman melebihi batas maksimal (Rp {THRESHOLD['max_loan_amount']:,})")
        
    if tenor < THRESHOLD["min_tenor"] or tenor > THRESHOLD["max_tenor"]:
        rejection_reasons.append(f"Tenor tidak valid (harus antara {THRESHOLD['min_tenor']} hingga {THRESHOLD['max_tenor']} bulan)")
        
    if employment_status != THRESHOLD["eligible_employment"]:
        rejection_reasons.append(f"Status pekerjaan tidak memenuhi syarat (harus '{THRESHOLD['eligible_employment']}')")

    # Tambahan logis: Cicilan tidak boleh lebih besar dari pendapatan bulanan
    if monthly_installment > monthly_income:
        rejection_reasons.append("Cicilan bulanan melebihi pendapatan bulanan Anda")

    # TODO: tampilkan hasil dan semua alasan penolakan
    print("\n" + "="*30)
    print("=== HASIL EVALUASI ===")
    print("="*30)
    print(f"Nama Customer   : {name}")
    print(f"Estimasi Cicilan: Rp {monthly_installment:,.2f} / bulan")

    if len(rejection_reasons) == 0:
        print("Status          : ✅ ELIGIBLE (DITERIMA)")
        print("Selamat! Pengajuan pinjaman Anda memenuhi semua kriteria.")
    else:
        print("Status          : ❌ NOT ELIGIBLE (DITOLAK)")
        print("\nAlasan penolakan:")
        for i, reason in enumerate(rejection_reasons, 1):
            print(f"{i}. {reason}")

except ValueError:
    print("\n[ERROR] Input tidak valid! Harap masukkan angka untuk nilai Pendapatan, Jumlah Pinjaman, dan Tenor.")
except Exception as e:
    print(f"\n[ERROR] Terjadi kesalahan sistem: {e}")