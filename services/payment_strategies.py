class PaymentStrategy:
    """
    Clase base para las estrategias de pago.
    Las subclases deberán sobrescribir el método pay.
    """

    PAGO_APROBADO = "APROBADO"
    PAGO_FALLIDO = "FALLIDO"
    PAGO_NO_IMPLEMENTADO = "NO_IMPLEMENTADO"

    def pay(self, payment_id, amount, q_payments=None):
        return {"status": self.PAGO_NO_IMPLEMENTADO}

# ------------------------------------------------------------------------------
class PayPalStrategy(PaymentStrategy):
    """
    Estrategia de pago utilizando PayPal como método.
    Condiciones:
        - Verifica que el pago sea menor de $ 5000
    """

    def pay(self, payment_id, amount, q_paypal_payments=None):
        if amount > 5000:
            return {"status": self.PAGO_FALLIDO}

        return {"status": self.PAGO_APROBADO}

# ------------------------------------------------------------------------------
class CreditCardStrategy(PaymentStrategy):
    """
    Estrategia de pago utilizando tarjeta de crédito como método.
    Condiciones:
        - Verifica que el pago sea menor de $ 10.000
        - Verifica que no haya más de 2 pagos registrados con tarjeta de crédito en estado "REGISTRADO"
    """

    def pay(self, payment_id, amount, q_creditcard_payments=None):
        if amount > 10000:
            return {"status": self.PAGO_FALLIDO}

        if q_creditcard_payments >= 2:
            return {"status": self.PAGO_FALLIDO}

        return {"status": self.PAGO_APROBADO}