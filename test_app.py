import unittest
from main import create_payment, update_payment, pay_payment, revert_payment, STATUS_REGISTRADO, STATUS_FALLIDO, STATUS_PAGADO
import asyncio


class TestApp(unittest.TestCase):

    def test_create_payment(self):
        
        response = asyncio.run(create_payment("test1", 100.0, "creditCard"))
        print(response)
        self.assertEqual(f"Pago test1 registrado con estado {STATUS_REGISTRADO}", response["message"])

    def test_update_payment(self):
        response = asyncio.run(update_payment("test1", amount=150.0))
        print(response)
        self.assertEqual(f"Pago test1 actualizado", response["message"])

    # def test_pay_payment(self):
    #     response = asyncio.run(pay_payment("test1"))
    #     print(response)
    #     self.assertEqual(f"Pago test1 procesado", response["message"])

    # def test_revert_payment(self):
    #     response = asyncio.run(revert_payment("test1"))
    #     self.assertEqual(f"Pago test1 revertido", response["message"])

if __name__ == "__main__":
    unittest.main()
