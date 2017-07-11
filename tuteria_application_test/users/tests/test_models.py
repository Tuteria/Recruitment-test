import os
from test_plus.test import TestCase
from unittest.mock import patch
from .factories import UserFactory, WalletFactory, WalletTransactionFactory, BookingFactory
from ..models import User, Booking, Wallet, WalletTransaction
from django.conf import settings


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()
        apps_dir = settings.APPS_DIR
        self.FILE = os.path.join(
            str(apps_dir), 'users', 'tests', 'test_mini.py')

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

    def test_if_test_mini_file_exists(self):

        self.assertTrue(os.path.exists(
            self.FILE), "You would need to create a test_mini.py file in this directory")

    def get_results_in_file(self):
        results = []
        with open(self.FILE) as fff:
            results = [x.strip() for x in fff]
        return results

    def test_there_is_a_function_called_fizzbuzz_val_in_test_mini_file(self):
        self.assertIn('def fizzbuzz_val(val):', self.get_results_in_file(),
                      "There must be a function named fizzbuzz_val which takes a param val in test_mini.py")

    def test_multiples_of_3_and_5_exists_in_file(self):
        results = self.get_results_in_file()
        self.assertIn('def test_multiples_of_3_and_5(self):', results,
                      "There is a test method called test_multiples_of_3_and_5")
        self.assertIn("self.assertEqual(fizzbuzz_val(15), 'FizzBuzz')", results,
                      "The test method asserts that fizzbuzz_val(15) return 'FizzBuzz'")

    def test_multiples_of_5_alone_exists_in_file(self):
        results = self.get_results_in_file()
        self.assertIn('def test_multiples_of_5_alone(self):', results,
                      'There is a test method called def test_multiples_of_5_alone')
        self.assertIn("self.assertTrue(fizzbuzz_val(5) is 'Buzz')", results,
                      "The tests assert that fizzbuzz_val(5) which equates to 'Buzz' is True")
        self.assertIn("self.assertTrue(fizzbuzz_val(10) is 'Buzz')", results,
                      "The tests assert that fizzbuzz_val(10) which equates to 'Buzz' is True")
        self.assertIn("self.assertTrue(fizzbuzz_val(20) is 'Buzz')", results,
                      "The tests assert that fizzbuzz_val(20) which equates to 'Buzz' is True")
        self.assertIn("self.assertFalse(fizzbuzz_val(8) is 'Buzz')", results,
                      "The tests assert that fizzbuzz_val(8) which equates to 'Buzz' is False")

    def test_multiples_of_3_alone_exists_in_file(self):
        results = self.get_results_in_file()
        self.assertIn('def test_multiples_of_3_alone(self):', results,
                      'There is a test method called def test_multiples_of_3_alone')
        self.assertIn("self.assertTrue(fizzbuzz_val(3) is 'Fizz')", results,
                      "The tests assert that fizzbuzz_val(3) which equates to 'Fizz' is True")
        self.assertIn("self.assertTrue(fizzbuzz_val(99) is 'Fizz')", results,
                      "The tests assert that fizzbuzz_val(99) which equates to 'Fizz' is True")
        self.assertIn("self.assertFalse(fizzbuzz_val(15) is 'Fizz')", results,
                      "The tests assert that fizzbuzz_val(15) which equates to 'Fizz' is False")
        self.assertIn("self.assertFalse(fizzbuzz_val(8) is 'Fizz')", results,
                      "The tests assert that fizzbuzz_val(8) which equates to 'Fizz' is False")

    def test_all_users_with_bookings_where_the_transaction_is_greater_than_one_is_fetched(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        booking1 = BookingFactory(user=user1)
        booking2 = BookingFactory(user=user2)
        booking3 = BookingFactory(user=user1)
        WalletTransactionFactory(wallet=user1.wallet, total=3000)
        WalletTransactionFactory(
            wallet=user1.wallet, total=5000, booking=booking1)
        WalletTransactionFactory(wallet=user1.wallet, total=3000)
        WalletTransactionFactory(
            wallet=user1.wallet, total=5000, booking=booking3)
        WalletTransactionFactory(wallet=user1.wallet, total=4000)
        WalletTransactionFactory(
            wallet=user2.wallet, total=2000, booking=booking2)
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

    def test_number_of_completed_and_cancelled_bookings_is_fetched(self):
        user1 = UserFactory()
        user2 = UserFactory()
        BookingFactory(user=user1, status=Booking.COMPLETED)
        BookingFactory(user=user1, status=Booking.SCHEDULED)
        BookingFactory(user=user1, status=Booking.CANCELLED)
        BookingFactory(user=user2, status=Booking.CANCELLED)
        BookingFactory(user=user1, status=Booking.CANCELLED)
        BookingFactory(user=user2, status=Booking.CANCELLED)
        BookingFactory(user=user1, status=Booking.CANCELLED)
        BookingFactory(user=user2, status=Booking.CANCELLED)
        BookingFactory(user=user1, status=Booking.CANCELLED)
        BookingFactory(user=user2, status=Booking.CANCELLED)
        BookingFactory(user=user1)
        BookingFactory(user=user2)
        BookingFactory(user=user1, status=Booking.COMPLETED)
        BookingFactory(user=user2, status=Booking.COMPLETED)
        self.assertFalse(hasattr(user1, 'completed'))
        self.assertFalse(hasattr(user2, 'completed'))
        self.assertFalse(hasattr(user1, 'scheduled'))
        self.assertFalse(hasattr(user2, 'scheduled'))
        self.assertFalse(hasattr(user2, 'not_started'))
        self.assertFalse(hasattr(user1, 'not_started'))
        self.assertFalse(hasattr(user2, 'cancelled'))
        self.assertFalse(hasattr(user1, 'cancelled'))
        users_with_booking_aggs = User.objects.bookings_aggs()
        first = [x for x in users_with_booking_aggs if x == user1][0]
        second = [x for x in users_with_booking_aggs if x == user2][0]
        self.assertEqual(first.completed, 2)
        self.assertEqual(second.completed, 1)
        self.assertEqual(first.cancelled, 4)
        self.assertEqual(second.cancelled, 4)
        self.assertEqual(first.scheduled, 1)
        self.assertEqual(second.scheduled, 0)
        self.assertEqual(first.not_started, 1)
        self.assertEqual(second.not_started, 1)
