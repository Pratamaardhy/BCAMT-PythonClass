class BankAccount:
    def __init__(self, nama_pemilik, saldo_awal=0):
        # Atribut (Data) milik objek
        self.nama_pemilik = nama_pemilik
        self.saldo = saldo_awal

    def cek_saldo(self):
        """Fitur untuk melihat informasi saldo saat ini"""
        print(f"\n[INFO] Saldo akun {self.nama_pemilik}: Rp {self.saldo:,.2f}")

    def setor_saldo(self, jumlah):
        """Fitur untuk menyetor uang ke rekening"""
        if jumlah > 0:
            self.saldo += jumlah
            print(f"\n[SUKSES] Berhasil setor Rp {jumlah:,.2f}.")
            self.cek_saldo()
        else:
            print("\n[GAGAL] Jumlah setoran harus lebih dari 0!")

    def tarik_saldo(self, jumlah):
        """Fitur untuk menarik uang dari rekening dengan validasi saldo"""
        if jumlah <= 0:
            print("\n[GAGAL] Jumlah penarikan harus lebih dari 0!")
        elif jumlah > self.saldo:
            print(f"\n[GAGAL] Penarikan gagal! Saldo Anda tidak mencukupi (Sisa saldo: Rp {self.saldo:,.2f})")
        else:
            self.saldo -= jumlah
            print(f"\n[SUKSES] Berhasil menarik Rp {jumlah:,.2f}.")
            self.cek_saldo()


# --- SIMULASI / DEMO PROGRAM ---
if __name__ == "__main__":
    print("=== SELAMAT DATANG DI BANK SEDERHANA ===")
    
    # 1. Membuat objek rekening baru atas nama "Ardi" dengan saldo awal Rp 500.000
    akun_ardi = BankAccount("Ardi Pratama", 500000)

    # 2. Cek saldo awal
    akun_ardi.cek_saldo()

    # 3. Melakukan setoran (menambah saldo) sebesar Rp 250.000
    akun_ardi.setor_saldo(250000)

    # 4. Melakukan penarikan saldo sebesar Rp 150.000
    akun_ardi.tarik_saldo(150000)

    # 5. Simulasi penarikan gagal (tarik melebihi saldo)
    akun_ardi.tarik_saldo(2000000)