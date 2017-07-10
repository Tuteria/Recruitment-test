import unittest

class FizzBuzzTest(unittest.TestCase):
    """
    Fizzbuzz TestCase
    """

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
    if val % 3 == 0 and val % 5 == 0:
        return 'FizzBuzz'
    elif val % 3 == 0:
        return 'Fizz'
    elif val % 5 == 0:
        return 'Buzz'
    else:
        return val

if __name__ == '__main__':
    unittest.main()