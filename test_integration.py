import unittest
import integration_testing as it

class TestTransferIntegration(unittest.TestCase):
    def setUp(self):
        self.repo = it.AccountRepository()
        self.service = it.TransferService(self.repo)

        # seed accounts
        self.repo.save('alice', 100)
        self.repo.save('bob', 50)

    def test_transfer_success(self):
        # positive case: normal transfer
        result = self.service.transfer('alice', 'bob', 30)
        self.assertEqual(result, "Transfer successful")
        self.assertEqual(self.repo.find_balance('alice'), 70)
        # expected receiver balance: 50 + 30 = 80
        self.assertEqual(self.repo.find_balance('bob'), 80)

    def test_sender_not_found(self):
        result = self.service.transfer('carol', 'bob', 10)
        self.assertEqual(result, "Sender not found")

    def test_receiver_not_found(self):
        result = self.service.transfer('alice', 'dave', 10)
        self.assertEqual(result, "Receiver not found")

    def test_invalid_amount_zero(self):
        result = self.service.transfer('alice', 'bob', 0)
        self.assertEqual(result, "Invalid amount")

    def test_invalid_amount_negative(self):
        result = self.service.transfer('alice', 'bob', -5)
        self.assertEqual(result, "Invalid amount")

    def test_insufficient_balance(self):
        result = self.service.transfer('bob', 'alice', 1000)
        self.assertEqual(result, "Insufficient balance")

if __name__ == '__main__':
    unittest.main()
