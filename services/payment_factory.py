from .payment_strategies import CreditCardStrategy, PayPalStrategy

class PaymentFactory:
    """
    Clase Factory para obtener la estrategia de pago adecuada según el método proporcionado.
    """
    @staticmethod
    def get_strategy(method: str):
        if method == "credit_card":
            return CreditCardStrategy()
        elif method == "paypal":
            return PayPalStrategy()
        else:
            raise ValueError("Método de pago no soportado")
