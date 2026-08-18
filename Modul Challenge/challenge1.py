# Challenge 1 — Memperbaiki Perhitungan Cicilan Loan

# Penjelasan Error
# Logical Error (Bunga Terlalu Besar): Pada starter code, annual_interest = principal * annual_interest_rate mengalikan langsung nilai persen (misal 12) dengan principal, bukan sebagai desimal.
# Runtime/Logical Error: Tidak adanya validasi membuat program error atau membagi dengan nol ketika tenor bernilai 0.

def calculate_monthly_installment(
    principal,
    annual_interest_rate,
    tenor_months
):
    if principal <= 0:
        raise ValueError("Pokok pinjaman harus lebih besar dari 0")
    if annual_interest_rate < 0:
        raise ValueError("Bunga tahunan tidak boleh negatif")
    if tenor_months <= 0:
        raise ValueError("Tenor harus lebih besar dari 0")

    annual_interest_decimal = annual_interest_rate / 100
    total_interest = principal * annual_interest_decimal * (tenor_months / 12)
    total_payment = principal + total_interest

    monthly_installment = total_payment / tenor_months
    return round(monthly_installment, 2)


if __name__ == "__main__":
    principal = 12_000_000
    annual_interest_rate = 12
    tenor_months = 12

    result = calculate_monthly_installment(
        principal,
        annual_interest_rate,
        tenor_months
    )

    print(f"Cicilan per bulan: Rp{result:,.2f}")