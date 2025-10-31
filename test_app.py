import unittest
import asyncio
from routers.payments_router import get_all_payments, create_payment, update_payment, pay_payment, revert_payment, STATUS_REGISTRADO, STATUS_FALLIDO, STATUS_PAGADO


class TestApp(unittest.TestCase):

    def test_get_payments(self):
        response = asyncio.run(get_all_payments())
        data = response["data"]
        # print(response)
        self.assertIsInstance(data, dict)

    def test_create_payment(self):
        response = asyncio.run(create_payment("2000", 200.0, "paypal"))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 2000 registrado con estado {STATUS_REGISTRADO}", message)

    def test_update_payment(self):
        response = asyncio.run(update_payment("2000", amount=250.0, payment_method="credit_card", status=STATUS_REGISTRADO))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 2000 actualizado con éxito", message)

    def test_pay_payment(self):
        response = asyncio.run(pay_payment("2000"))
        message = response["message"]
        print(response)
        self.assertIn(f"Pago 2000 procesado con éxito", message)

    def test_revert_payment(self):
        response = asyncio.run(update_payment("2000", amount=250.0, payment_method="credit_card", status=STATUS_REGISTRADO))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 2000 no se puede revertir porque no está en estado {STATUS_FALLIDO}", message)

if __name__ == "__main__":
    unittest.main()
