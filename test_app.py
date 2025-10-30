import tempfile
import os
import json
import unittest
import asyncio
import main


class TestApp(unittest.TestCase):
    
    def setUp(self):
        # Crear un archivo temporal y cerrarlo inmediatamente
        fd, path = tempfile.mkstemp()
        os.close(fd)  # 🔥 importante para Windows
        self.tempfile = path

        # Inicializar con un JSON vacío
        with open(self.tempfile, "w") as f:
            json.dump({}, f)

        main.DATA_PATH = self.tempfile  # Reemplaza el archivo de datos

    def tearDown(self):
        # Borrar el archivo temporal al finalizar
        if os.path.exists(self.tempfile):
            os.remove(self.tempfile)


    def test_create_payment(self):
        response = asyncio.run(main.create_payment("test1", 100.0, "creditCard"))
        print(response)
        self.assertEqual(response["message"], "Pago test1 registrado con exito")

    def test_update_payment(self):
        asyncio.run(main.create_payment("test1", 100.0, "creditCard"))
        response = asyncio.run(main.update_payment("test1", amount=150.0))
        print(response)
        self.assertEqual(response["message"], "Pago test1 actualizado")

    def test_pay_payment(self):
        asyncio.run(main.create_payment("test17", 100.0, "creditCard"))
        response = asyncio.run(main.pay_payment("test17"))
        print(response)
        self.assertEqual(response["message"], "Pago test17 procesado")

    def test_revert_payment(self):
        asyncio.run(main.create_payment("test30", 100.0, "creditCard"))
        data = main.load_all_payments()
        data["test30"]["status"] = main.STATUS_FALLIDO
        main.save_all_payments(data)
        response = asyncio.run(main.revert_payment("test30"))
        print(response)
        self.assertEqual(response["message"], "Pago test30 revertido")


if __name__ == "__main__":
    unittest.main()
