package oop2.model;

public class creditCardPayment extends payment {
    private String cardNumber;

    public creditCardPayment() {
    }

    public creditCardPayment(double amount, String cardNumber) {
        super(amount);
        this.cardNumber = cardNumber;
    }

    public String getCardNumber() {
        return cardNumber;
    }

    public void setCardNumber(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    @Override
    public String processPayment() {
        String lastFour = (cardNumber != null && cardNumber.length() >= 4)
                ? cardNumber.substring(cardNumber.length() - 4)
                : cardNumber;
        return "Memproses PKartu Kredit (**** " + lastFour + ") | Status: BERHASIL!";
    }
}