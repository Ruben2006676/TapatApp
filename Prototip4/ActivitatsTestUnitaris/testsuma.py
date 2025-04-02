import unittest

def suma(a, b):
    """Retorna la suma de dos números."""
    return a + b

class TestOperacions(unittest.TestCase):
    
    def test_suma(self):
        # Probar suma de números positivos
        self.assertEqual(suma(3, 4), 7)
        
        # Probar suma de números negativos
        self.assertEqual(suma(-1, 1), 0)
        
        # Probar suma de ceros
        self.assertEqual(suma(0, 0), 0)
        
if __name__ == '__main__':
    unittest.main()
