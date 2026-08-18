# Challenge 3 — Unit Test Loan-to-Value

def calculate_ltv(loan_amount, asset_value):
    if asset_value <= 0:
        raise ValueError("Nilai aset harus lebih besar dari 0")
    if loan_amount < 0:
        raise ValueError("Nilai pinjaman tidak boleh negatif")

    ltv = (loan_amount / asset_value) * 100
    return round(ltv, 2)


def is_ltv_eligible(loan_amount, asset_value):
    return calculate_ltv(loan_amount, asset_value) <= 80