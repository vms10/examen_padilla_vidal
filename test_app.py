import unittest
import asyncio
from routers.payments_router import get_all_payments, create_payment, update_payment, pay_payment, revert_payment, STATUS_REGISTRADO, STATUS_FALLIDO, STATUS_PAGADO


class TestApp(unittest.TestCase):

    # 1. Test creación de un pago
    def test_create_payment(self):
        response = asyncio.run(create_payment("1000", 200.0, "paypal"))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 1000 registrado con estado {STATUS_REGISTRADO}", message)

    # 2. Test modificación de un pago permitida
    def test_update_payment_allowed(self):
        response = asyncio.run(update_payment("1000", amount=250.0, payment_method="credit_card", status=STATUS_REGISTRADO))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 1000 actualizado con éxito", message)

    # 3. Test pago permitido
    def test_pay_payment_allowed(self):
        response = asyncio.run(pay_payment("1000"))
        message = response["message"]
        print(response)
        self.assertIn(f"Pago 1000 procesado con éxito", message)

    # 4. Test modificación de un pago NO permitida
    def test_update_payment_not_allowed(self):
        response = asyncio.run(update_payment("1000", amount=300.0, payment_method="credit_card", status=STATUS_REGISTRADO))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 1000 no se puede actualizar porque no está en estado {STATUS_REGISTRADO}", message)

    # =======================================================================================================================

    # 5. Test creación de un pago
    def test_create_payment(self):
        response = asyncio.run(create_payment("2000", 45000.0, "credit_card"))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 2000 registrado con estado {STATUS_REGISTRADO}", message)

    # 6. Test pago fallido
    def test_pay_payment_failed(self):
        response = asyncio.run(pay_payment("2000"))
        message = response["message"]
        print(response)
        self.assertIn(f"Pago 2000 fallido durante el procesamiento", message)

    # 7. Test reversión de un pago
    def test_revert_payment(self):
        response = asyncio.run(update_payment("2000", amount=45000.0, payment_method="credit_card", status=STATUS_FALLIDO))
        message = response["message"]
        # print(response)
        self.assertEqual(f"Pago 2000 actualizado con éxito", message)

    # =======================================================================================================================

    def test_get_payments(self):
        response = asyncio.run(get_all_payments())
        data = response["data"]
        # print(response)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
