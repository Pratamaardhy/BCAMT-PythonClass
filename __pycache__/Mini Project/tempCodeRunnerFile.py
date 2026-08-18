def tampilkan_menu():
    print("\n==============================")
    print("   APLIKASI TO-DO LIST SAYA   ")
    print("==============================")
    print("1. Lihat Daftar Tugas")
    print("2. Tambah Tugas Baru")
    print("3. Ubah / Edit Tugas")
    print("4. Hapus Tugas")
    print("5. Keluar")

def main():
    # List utama untuk menyimpan data tugas
    daftar_tugas = []

    while True:
        tampilkan_menu()
        pilihan = input("\nPilih menu (1-5): ")

        if pilihan == "1":
            # --- 1. MELIHAT DAFTAR TUGAS ---
            print("\n--- DAFTAR TUGAS ANDA ---")
            if len(daftar_tugas) == 0:
                print("Belum ada tugas yang tersimpan.")
            else:
                # Menggunakan enumerate untuk menampilkan nomor urut mulai dari 1
                for index, tugas in enumerate(daftar_tugas, start=1):
                    print(f"{index}. {tugas}")

        elif pilihan == "2":
            # --- 2. MENAMBAH TUGAS BARU (Append) ---
            tugas_baru = input("\nMasukkan nama tugas baru: ")
            if tugas_baru.strip() != "":
                daftar_tugas.append(tugas_baru)  # Menambahkan data ke dalam list
                print(f"Tugas '{tugas_baru}' berhasil ditambahkan!")
            else:
                print("Nama tugas tidak boleh kosong!")

        elif pilihan == "3":
            # --- 3. MENGUBAH / EDIT TUGAS (Modify list by index) ---
            print("\n--- UBAH TUGAS ---")
            if len(daftar_tugas) == 0:
                print("Belum ada tugas untuk diubah.")
            else:
                for index, tugas in enumerate(daftar_tugas, start=1):
                    print(f"{index}. {tugas}")
                
                try:
                    nomor = int(input("\nPilih nomor tugas yang ingin diubah: "))
                    if 1 <= nomor <= len(daftar_tugas):
                        tugas_baru = input("Masukkan nama tugas yang baru: ")
                        # Mengubah isi list berdasarkan indeks (indeks mulai dari 0, maka nomor - 1)
                        daftar_tugas[nomor - 1] = tugas_baru
                        print("Tugas berhasil diperbarui!")
                    else:
                        print("Nomor tugas tidak valid.")
                except ValueError:
                    print("Mohon masukkan angka yang valid.")

        elif pilihan == "4":
            # --- 4. MENGHAPUS TUGAS (Remove / Pop) ---
            print("\n--- HAPUS TUGAS ---")
            if len(daftar_tugas) == 0:
                print("Belum ada tugas untuk dihapus.")
            else:
                for index, tugas in enumerate(daftar_tugas, start=1):
                    print(f"{index}. {tugas}")
                
                try:
                    nomor = int(input("\nPilih nomor tugas yang ingin dihapus: "))
                    if 1 <= nomor <= len(daftar_tugas):
                        # Menghapus item dari list menggunakan pop() berdasarkan indeks
                        tugas_terhapus = daftar_tugas.pop(nomor - 1)
                        print(f"Tugas '{tugas_terhapus}' berhasil dihapus!")
                    else:
                        print("Nomor tugas tidak valid.")
                except ValueError:
                    print("Mohon masukkan angka yang valid.")

        elif pilihan == "5":
            # --- 5. KELUAR APLIKASI ---
            print("\nTerima kasih telah menggunakan aplikasi To-Do List!")
            break
        else:
            print("\nPilihan tidak valid. Silakan pilih angka 1 sampai 5.")

if __name__ == "__main__":
    main()