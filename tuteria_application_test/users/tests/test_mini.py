from test_plus.test import TestCase

def fizzbuzz_val(val):
    if val%5==0 and val%3==0:
        return 'FizzBuzz'
    elif val%5==0:
        return 'Buzz'
    elif val%3==0:
        return 'Fizz'
    else:
        return

class TestUser(TestCase):
    def test_multiples_of_3_and_5(self):
        self.assertEqual(fizzbuzz_val(15), 'FizzBuzz')

    def test_multiples_of_5_alone(self):
        self.assertTrue(fizzbuzz_val(5) is 'Buzz')
        self.assertTrue(fizzbuzz_val(10) is 'Buzz')
        self.assertTrue(fizzbuzz_val(20) is 'Buzz')
        self.assertFalse(fizzbuzz_val(8) is 'Buzz')

    def test_multiples_of_3_alone(self):
        self.assertTrue(fizzbuzz_val(3) is 'Fizz')
        self.assertTrue(fizzbuzz_val(99) is 'Fizz')
        self.assertFalse(fizzbuzz_val(15) is 'Fizz')
        self.assertFalse(fizzbuzz_val(8) is 'Fizz')

