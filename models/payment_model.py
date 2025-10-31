# app/models/payment_model.py

class Payment:
    """
    Modelo de dominio que representa un pago.
    """

    def __init__(self, payment_id: str, amount: float, method: str, status: str = "REGISTRADO"):
        self.payment_id = payment_id
        self.amount = amount
        self.method = method
        self.status = status

    def to_dict(self):
        """
        Convierte el objeto a diccionario (para guardarlo en JSON).
        """

        return {
            "payment_id": self.payment_id,
            "amount": self.amount,
            "payment_method": self.method,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea un Payment a partir de un diccionario cargado desde JSON.
        """
        
        return cls(
            payment_id=data.get("payment_id"),
            amount=data.get("amount"),
            method=data.get("payment_method"),
            status=data.get("status", "REGISTRADO")
        )
