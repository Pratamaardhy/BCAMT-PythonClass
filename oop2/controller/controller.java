package oop2.controller;

import oop2.model.payment;
import java.util.ArrayList;
import java.util.List;

public class controller {
    private List<payment> paymentHistory = new ArrayList<>();

    public void addPayment(payment payment) throws Exception {
        if (payment.getAmount() <= 0) {
            throw new Exception("Jumlah pembayaran harus lebih dari 0!");
        }
        paymentHistory.add(payment);
        System.out.println("-> " + payment.processPayment());
    }

    public List<payment> getPaymentHistory() throws Exception {
        if (paymentHistory.isEmpty()) {
            throw new Exception("Belum ada riwayat transaksi.");
        }
        return paymentHistory;
    }
}