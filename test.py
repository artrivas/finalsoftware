import unittest
import pruebas
class TestSample(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_contactos(self):
        result = test_get_cuenta("123")
        self.assertEqual(result["status"], "successfull")  # Diferente de vacío

    def test_failed_contactos(self):
        result = test_get_cuenta("1234")
        self.assertEqual(result["status"], "error")#valida si es igual   Equal=igual
    
    def test_failed_historial(self):
        result = test_get_historial("1234")
        self.assertEqual(result["status"], "error")#valida si es igual   Equal=igual
    

    def test_failed_pagar(self):
        result = test_pagar_cuenta("2134", "3214",200)
        self.assertEqual(result["status"], "error")

    def tearDown(self):
        pass