package oop2.model;

public class eWalletPayment extends payment {
    private String walletProvider;
    private String phoneNumber;


    public eWalletPayment(double amount, String walletProvider, String phoneNumber) {
        super(amount);
        this.walletProvider = walletProvider;
        this.phoneNumber = phoneNumber;
    }

    public String getWalletProvider() {
        return walletProvider;
    }

    public void setWalletProvider(String walletProvider) {
        this.walletProvider = walletProvider;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    @Override
    public String processPayment() {
        return "Memproses Pembayaran E-Wallet (" + walletProvider + " - " + phoneNumber + ") | Status: BERHASIL!";
    }
}