# Challenge 2 — Memperbaiki Perhitungan Total Tagihan

def calculate_final_bill(
    price,
    quantity,
    discount_percent,
    tax_percent
):
    try:
        qty = int(quantity)
    except (ValueError, TypeError):
        raise ValueError("Quantity harus berupa angka yang valid")

    if qty <= 0:
        raise ValueError("Quantity harus lebih besar dari 0")
    if not (0 <= discount_percent <= 100):
        raise ValueError("Diskon harus di antara 0 sampai 100 persen")
    if tax_percent < 0:
        raise ValueError("Pajak tidak boleh negatif")

    subtotal = price * qty
    discount = subtotal * (discount_percent / 100)
    discounted_subtotal = subtotal - discount
    tax = discounted_subtotal * (tax_percent / 100)
    final_bill = discounted_subtotal + tax

    return round(subtotal, 2), round(discount, 2), round(tax, 2), round(final_bill, 2)


if __name__ == "__main__":
    sub, disc, tx, total = calculate_final_bill(
        price=250_000,
        quantity="2",
        discount_percent=10,
        tax_percent=11
    )

    print(f"Subtotal: Rp{sub:,.2f}")
    print(f"Diskon: Rp{disc:,.2f}")
    print(f"Pajak: Rp{tx:,.2f}")
    print(f"Total tagihan: Rp{total:,.2f}")