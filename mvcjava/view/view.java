package mvcjava.view;

import mvcjava.controller.controller;
import mvcjava.model.model;
import java.util.Scanner;

public class view {
    private controller controller;
    private Scanner scanner;

    public view(controller controller) {
        this.controller = controller;
        this.scanner = new Scanner(System.in);
    }

    public void showMenu() {
        int pilih = 0;
        do {
            System.out.println("\n=== APLIKASI MANAJEMEN KARYAWAN ===");
            System.out.println("1. Tambah Karyawan");
            System.out.println("2. Lihat Semua Karyawan");
            System.out.println("3. Ubah Karyawan");
            System.out.println("4. Hapus Karyawan");
            System.out.println("5. Keluar");
            System.out.print("Pilih (1-5): ");

            try {
                pilih = Integer.parseInt(scanner.nextLine());
                switch (pilih) {
                    case 1:
                        System.out.print("ID: "); String id = scanner.nextLine();
                        System.out.print("Nama: "); String nama = scanner.nextLine();
                        System.out.print("Jabatan: "); String jabatan = scanner.nextLine();
                        controller.tambah(id, nama, jabatan);
                        break;
                    case 2:
                        for (model k : controller.tampilkan()) {
                            System.out.println(k);
                        }
                        break;
                    case 3:
                        System.out.print("ID Karyawan yang diubah: "); String idUbah = scanner.nextLine();
                        System.out.print("Nama Baru: "); String nBaru = scanner.nextLine();
                        System.out.print("Jabatan Baru: "); String jBaru = scanner.nextLine();
                        controller.ubah(idUbah, nBaru, jBaru);
                        break;
                    case 4:
                        System.out.print("ID Karyawan yang dihapus: "); String idHapus = scanner.nextLine();
                        controller.hapus(idHapus);
                        break;
                    case 5:
                        System.out.println("Selesai!");
                        break;
                    default:
                        System.out.println("Pilihan tidak valid!");
                }
            } catch (Exception e) {
                System.out.println("[Error] " + e.getMessage());
            }
        } while (pilih != 5);
    }
}
