import unittest
import asyncio
from routers.payments_router import get_all_payments, create_payment, update_payment, pay_payment, revert_payment, STATUS_REGISTRADO, STATUS_FALLIDO, STATUS_PAGADO


class TestApp(unittest.TestCase):


    # 1. Test creación de un pago #1000
    def test_create_payment_01(self):
        response = asyncio.run(create_payment("1000", 200000.0, "credit_card"))
        message = response["message"]
        print(f"Test #1.1: {response}")
        self.assertEqual(f"Pago 1000 registrado con estado {STATUS_REGISTRADO}", message)

    # 1. Test creación de un pago #2000
    def test_create_payment_02(self):
        response = asyncio.run(create_payment("2000", 45000.0, "paypal"))
        message = response["message"]
        print(f"Test #1.2: {response}")
        self.assertEqual(f"Pago 2000 registrado con estado {STATUS_REGISTRADO}", message)

    # 1. Test creación de un pago #3000
    def test_create_payment_03(self):
        response = asyncio.run(create_payment("3000", 300.0, "paypal"))
        message = response["message"]
        print(f"Test #1.3: {response}")
        self.assertEqual(f"Pago 3000 registrado con estado {STATUS_REGISTRADO}", message)

    # 2. Test modificación de un pago permitida
    def test_update_payment_allowed(self):
        response = asyncio.run(update_payment("1000", amount=250.0, payment_method="credit_card", status=STATUS_REGISTRADO))
        message = response["message"]
        print(f"Test #2.1: {response}")
        self.assertEqual(f"Pago 1000 actualizado con éxito", message)

    # 2. Test modificación de un pago NO permitida
    def test_update_payment_not_allowed(self):
        response = asyncio.run(update_payment("1001", amount=35000.0, payment_method="paypal", status=STATUS_REGISTRADO))
        message = response["message"]
        print(f"Test #2.2: {response}")
        self.assertEqual(f"Pago 1001 no encontrado", message)

    # 3. Test pago permitido
    def test_pay_payment_allowed(self):
        response = asyncio.run(pay_payment("3000"))
        message = response["message"]
        print(f"Test #3.1: {response}")
        self.assertIn(f"Pago 3000 procesado con éxito", message)

    # 3. Test pago NO permitido
    def test_pay_payment_not_allowed(self):
        response = asyncio.run(pay_payment("2000"))
        message = response["message"]
        print(f"Test #3.2: {response}")
        self.assertEqual(f"Pago 2000 fallido durante el procesamiento", message)

    # 4. Test reversión de un pago
    def test_revert_payment(self):
        response = asyncio.run(revert_payment("2000"))
        message = response["message"]
        print(f"Test #4: {response}")
        self.assertEqual(f"Pago 2000 revertido con éxito", message)

    # 5. Test obtención de todos los pagos
    def test_get_payments(self):
        response = asyncio.run(get_all_payments())
        data = response["data"]
        print(f"Test #5: {response}")
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    # 0. Setup inicial: limpiar el archivo data.json
    def setUp(self):
        with open("data.json", "w") as f:
            f.write("{}")
            f.close()

    unittest.main()
