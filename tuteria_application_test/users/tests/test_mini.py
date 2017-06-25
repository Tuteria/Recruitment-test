"""Fizzbuzz test."""

import unittest

class FizzBuzzTest(unittest.TestCase):
    """TestCase for fizzbuzz_val."""

    def test_multiples_of_3_alone(self):
        """Tests multiples of 3 alone."""
        self.assertTrue(fizzbuzz_val(3) is 'Fizz')
        self.assertFalse(fizzbuzz_val(8) is 'Fizz')
        self.assertFalse(fizzbuzz_val(15) is 'Fizz')
        self.assertTrue(fizzbuzz_val(99) is 'Fizz')

    def test_multiples_of_5_alone(self):
        """Tests multiples of 5 alone."""
        self.assertTrue(fizzbuzz_val(5) is 'Buzz')
        self.assertFalse(fizzbuzz_val(8) is 'Buzz')
        self.assertTrue(fizzbuzz_val(10) is 'Buzz')
        self.assertTrue(fizzbuzz_val(20) is 'Buzz')

    def test_multiples_of_3_and_5(self):
        """Tests multiples of 3 and 5."""
        self.assertEqual(fizzbuzz_val(15), 'FizzBuzz')

def fizzbuzz_val(val):
    """Fizzbuzz function."""
    result = ''

    if val >=3:
        if not val % 3:
            result+='Fizz'

        if not val % 5:
            result+='Buzz'

    return result or False

if __name__ == '__main__':
    unittest.main()