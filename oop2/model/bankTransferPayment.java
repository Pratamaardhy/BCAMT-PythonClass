package oop2.model;

public class bankTransferPayment extends payment {
    private String bankName;
    private String accountNumber;

    public bankTransferPayment() {
    }

    public bankTransferPayment(double amount, String bankName, String accountNumber) {
        super(amount);
        this.bankName = bankName;
        this.accountNumber = accountNumber;
    }

    public String getBankName() {
        return bankName;
    }

    public void setBankName(String bankName) {
        this.bankName = bankName;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public void setAccountNumber(String accountNumber) {
        this.accountNumber = accountNumber;
    }
    @Override
    public String processPayment() {
        return "Memproses Transfer Bank (" + bankName + " - " + accountNumber + ") | Status: BERHASIL!";
    }
}