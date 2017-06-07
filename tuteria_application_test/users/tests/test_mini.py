import os
from test_plus.test import TestCase



# def fizzbuzz_val(val):
# 	if val == 15:
# 		return 'FizzBuzz'

# 	if val == 8:
# 		return 'FizzBuzz'

# 	if val == 5:
# 		return 'Buzz'

# 	if val ==10:
# 		return 'Buzz'

# 	if val == 20:
# 		return 'Buzz'

# 	if val == 99:
# 		return 'Fizz'

# 	if val ==3:
# 		return 'Fizz'

def fizzbuzz_val(val):
	fizzbuzz = []
	if val:
		if val%5 == 0:
			fizzbuzz.append('Buzz')

		if val%3 == 0:
			fizzbuzz.append('Fizz')

	if len(fizzbuzz) == 0:
		return None
	
	if len(fizzbuzz)==1:
		return fizzbuzz[0]

	elif len(fizzbuzz)==2:
		return fizzbuzz[1] + fizzbuzz[0]

		



class MiniTest(TestCase):

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