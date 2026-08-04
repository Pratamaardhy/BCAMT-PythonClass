package oop2.view;

import oop2.controller.controller;
import oop2.model.bankTransferPayment;
import oop2.model.creditCardPayment;
import oop2.model.eWalletPayment;
import oop2.model.payment;

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
            System.out.println("\n=== SISTEM PEMBAYARAN (MVC TANPA LOMBOK) ===");
            System.out.println("1. Bayar via Kartu Kredit");
            System.out.println("2. Bayar via Transfer Bank");
            System.out.println("3. Bayar via E-Wallet");
            System.out.println("4. Lihat Riwayat Pembayaran");
            System.out.println("5. Keluar");
            System.out.print("Pilih Menu (1-5): ");

            try {
                pilih = Integer.parseInt(scanner.nextLine());
                switch (pilih) {
                    case 1:
                        payCreditCard();
                        break;
                    case 2:
                        payBankTransfer();
                        break;
                    case 3:
                        payEWallet();
                        break;
                    case 4:
                        showHistory();
                        break;
                    case 5:
                        System.out.println("Terima kasih, transaksi selesai!");
                        break;
                    default:
                        System.out.println("Pilihan tidak valid!");
                }
            } catch (Exception e) {
                System.out.println("[Error] " + e.getMessage());
            }
        } while (pilih != 5);
    }

    private void payCreditCard() throws Exception {
        System.out.print("Jumlah Bayar: "); double amount = Double.parseDouble(scanner.nextLine());
        System.out.print("Nomor Kartu: "); String cardNum = scanner.nextLine();
        controller.addPayment(new creditCardPayment(amount, cardNum));
    }

    private void payBankTransfer() throws Exception {
        System.out.print("Jumlah Bayar: "); double amount = Double.parseDouble(scanner.nextLine());
        System.out.print("Nama Bank: "); String bank = scanner.nextLine();
        System.out.print("Nomor Rekening: "); String acc = scanner.nextLine();
        controller.addPayment(new bankTransferPayment(amount, bank, acc));
    }

    private void payEWallet() throws Exception {
        System.out.print("Jumlah Bayar: "); double amount = Double.parseDouble(scanner.nextLine());
        System.out.print("Provider (GoPay/OVO/DANA): "); String provider = scanner.nextLine();
        System.out.print("Nomor HP: "); String phone = scanner.nextLine();
        controller.addPayment(new eWalletPayment(amount, provider, phone));
    }

    private void showHistory() {
        try {
            System.out.println("\n--- RIWAYAT TRANSAKSI ---");
            for (payment p : controller.getPaymentHistory()) {
                System.out.println(p.printReceipt());
            }
        } catch (Exception e) {
            System.out.println("[Info] " + e.getMessage());
        }
    }
}