package oop2.model;

public abstract class payment {
    private double amount;

    public payment() {
    }

    public payment(double amount) {
        this.amount = amount;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public abstract String processPayment();
    public String printReceipt() {
        return "Total Transaksi: Rp " + amount;
    }
}