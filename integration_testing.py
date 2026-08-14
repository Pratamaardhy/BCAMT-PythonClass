class AccountRepository:
    def __init__(self):
        self.accounts = {}

    def save(self, account_id, balance):
        self.accounts[account_id] = balance

    def find_balance(self, account_id):
        return self.accounts.get(account_id)

class TransferService:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def transfer(self, sender_id, receiver_id, amount):
        sender_balance = self.account_repository.find_balance(sender_id)
        receiver_balance = self.account_repository.find_balance(receiver_id)

        if sender_balance is None:
            return "Sender not found"

        if receiver_balance is None:
            return "Receiver not found"

        if amount <= 0:
            return "Invalid amount"

        if sender_balance < amount:
            return "Insufficient balance"

        new_sender_balance = sender_balance - amount

        # Intentional bug:
        # # Saldo penerima bertambah dua kali lipat
        # new_receiver_balance = receiver_balance + (amount * 2)

        # Fix: penerima hanya bertambah sebesar `amount` (tidak dua kali)
        new_receiver_balance = receiver_balance + amount

        self.account_repository.save(
            sender_id,
            new_sender_balance
        )

        self.account_repository.save(
            receiver_id,
            new_receiver_balance
        )

        return "Transfer successful"