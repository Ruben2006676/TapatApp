import unittest

def suma(a, b):
    """Retorna la suma de dos números."""
    return a + b

def resta(a, b):
    """Retorna la resta de dos números."""
    return a - b

def divideix(a, b):
    """Retorna la división de dos números. Retorna 'Error' si b es 0."""
    if b == 0:
        return "Error: divisió per zero"
    return a / b

class TestOperacions(unittest.TestCase):

    def test_suma(self):
        self.assertEqual(suma(3, 4), 7)
        self.assertEqual(suma(-1, 1), 0)
        self.assertEqual(suma(0, 0), 0)
        
    def test_resta(self):
        self.assertEqual(resta(10, 5), 5)
        self.assertEqual(resta(0, 0), 0)
        self.assertEqual(resta(5, 10), -5)
        
    def test_divideix(self):
        self.assertEqual(divideix(10, 2), 5)
        self.assertEqual(divideix(5, 0), "Error: divisió per zero")
        self.assertEqual(divideix(0, 5), 0)
        
if __name__ == '__main__':
    unittest.main()
