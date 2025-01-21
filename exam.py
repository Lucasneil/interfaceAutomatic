import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestStringMethods('test_upper'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
