from test_plus.test import TestCase
from unittest.mock import patch
from .factories import UserFactory, WalletFactory, WalletTransactionFactory, BookingFactory
from ..models import User, Booking, Wallet, WalletTransaction


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )

    def test_all_users_with_bookings_where_the_transaction_is_greater_than_one_is_fetched(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        booking1 = BookingFactory(user=user1)
        booking2 = BookingFactory(user=user2)
        booking3 = BookingFactory(user=user1)
        WalletTransactionFactory(wallet=user1.wallet, total=3000)
        WalletTransactionFactory(wallet=user1.wallet, total=5000, booking=booking1)
        WalletTransactionFactory(wallet=user1.wallet, total=3000)
        WalletTransactionFactory(wallet=user1.wallet, total=5000, booking=booking3)
        WalletTransactionFactory(wallet=user1.wallet, total=4000)
        WalletTransactionFactory(wallet=user2.wallet, total=2000, booking=booking2)
        WalletTransactionFactory(wallet=user3.wallet, total=4000)
        users_with_bookings = User.g_objects.with_bookings()
        self.assertEqual(
            users_with_bookings.count(), 2
        )
        self.assertIn(user1, users_with_bookings)
        self.assertIn(user2, users_with_bookings)
        users_with_total_transactions = User.g_objects.with_transaction_total()
        self.assertEqual(
            users_with_total_transactions[0].transaction_total, 20000
        )
        users_with_transaction_and_booking = User.g_objects.with_transaction_and_booking()
        self.assertIn(user1, users_with_transaction_and_booking)
        self.assertIn(user2, users_with_transaction_and_booking)
        users_with_no_bookings = User.g_objects.no_bookings()
        self.assertEqual(user3, users_with_no_bookings.first())
        self.assertEqual(
            users_with_no_bookings.first().transaction_total, 4000
        )

    def test_no_transaction_total_property_in_user_model(self):
        self.assertFalse(hasattr(self.user, 'transaction_total'))
