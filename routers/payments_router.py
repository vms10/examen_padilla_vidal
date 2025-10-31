from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from repository.payment_repository import load_all_payments, load_payment, save_payment
from services.payment_factory import PaymentFactory

app = FastAPI()
router = APIRouter()

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

# Test del servidor
@router.get("/")
async def prueba_root():
    return {"message": "Servidor activo"}

# GET en el path "/payments" que retorne todos los pagos.
@router.get("/payments")
async def get_all_payments():
    data = {"data": load_all_payments()}
    return data


# POST en el path /payments/{payment_id} que registre un nuevo pago.
@router.post("/payments/{payment_id}")
async def create_payment(payment_id: str, amount: float, payment_method: str):
    payment_data = {
        "amount": amount,
        "payment_method": payment_method,
        "status": STATUS_REGISTRADO
    }
    save_payment(payment_id, payment_data)
    return {"message": f"Pago {payment_id} registrado con estado {STATUS_REGISTRADO}"}


# POST en el path /payments/{payment_id}/update que cambie los parametros de una pago (amount, payment_method)
@router.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float = None, payment_method: str = None, status: str = None):
    # payment_data = load_all_payments().get(payment_id)
    payment_data = load_payment(payment_id)
    
    if not payment_data:
        return {"message": f"Pago {payment_id} no encontrado"}
    else:
        if payment_data["status"] != STATUS_REGISTRADO:
            return {"message": f"Pago {payment_id} no se puede actualizar porque no está en estado {STATUS_REGISTRADO}"}
        else:
            if amount is None or payment_method is None or status is None:
                return {"message": f"Pago {payment_id} no se puede actualizar porque faltan algunos parámetros"}
            
            payment_data["amount"] = amount
            payment_data["payment_method"] = payment_method
            payment_data["status"] = status

            save_payment(payment_id, payment_data)
            return {"message": f"Pago {payment_id} actualizado con éxito"}


# POST en el path /payments/{payment_id}/pay que intente.
@router.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    # payment_data = load_all_payments().get(payment_id)
    payment_data = load_payment(payment_id)

    if not payment_data:
        return {"message": f"Pago {payment_id} no encontrado"}
    else:
        strategy = PaymentFactory.get_strategy(payment_data["payment_method"])

        if not strategy:
            return {"message": f"Pago {payment_id} no se puede pagar porque el método de pago no está soportado"}
        
        if payment_data["status"] != STATUS_REGISTRADO:
            return {"message": f"Pago {payment_id} no se puede procesar porque no está en estado {STATUS_REGISTRADO}"} 
        
        if payment_data["payment_method"] == "credit_card":
            q_creditcard_payments = sum(1 for p in load_all_payments().values() if p["payment_method"] == "credit_card" and p["status"] == STATUS_REGISTRADO)
            result = strategy.pay(payment_id, payment_data["amount"], q_creditcard_payments)
        else:
            result = strategy.pay(payment_id, payment_data["amount"])

        if result["status"] == strategy.PAGO_APROBADO:
            payment_data["status"] = STATUS_PAGADO
            save_payment(payment_id, payment_data)
            return {"message": f"Pago {payment_id} procesado con éxito"}
        else:
            payment_data["status"] = STATUS_FALLIDO
            save_payment(payment_id, payment_data)
            return {"message": f"Pago {payment_id} fallido durante el procesamiento"}
        

# POST en el path /payments/{payment_id}/revert que revertir el pago.
@router.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    payment_data = load_payment(payment_id)

    if not payment_data:
        return {"message": f"Pago {payment_id} no encontrado"}
    else:
        if payment_data["status"] != STATUS_FALLIDO:
            return {"message": f"Pago {payment_id} no se puede revertir porque no está en estado {STATUS_FALLIDO}"}
        else:
            payment_data["status"] = STATUS_REGISTRADO
            save_payment(payment_id, payment_data)
            return {"message": f"Pago {payment_id} revertido con éxito"}
