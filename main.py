import json
from fastapi import FastAPI

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"

app = FastAPI()


def load_all_payments():
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


def save_all_payments(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_payment(payment_id):
    data = load_all_payments()[payment_id]
    return data


def save_payment_data(payment_id, data):
    all_data = load_all_payments()
    all_data[str(payment_id)] = data
    save_all_payments(all_data)


def save_payment(payment_id, amount, payment_method, status):
    data = {
        AMOUNT: amount,
        PAYMENT_METHOD: payment_method,
        STATUS: status,
    }
    save_payment_data(payment_id, data)


# GET en el path /payments que retorne todos los pagos.
@app.get("/payments")
async def get_all_payments():
    data = {"data": load_all_payments()}
    return data


# POST en el path /payments/{payment_id} que registre un nuevo pago.
@app.post("/payments/{payment_id}")
async def create_payment(payment_id: str, amount: float, payment_method: str):
    # ---  Validar argumentos ---
    if amount is None or amount <= 0:
        return {"message": "El monto debe ser un número positivo."}
    if not payment_method:
        return {"message": "Debe especificarse el método de pago."}
    if not payment_id:
        return {"message": "Debe especificarse el payment_id."}

    # ---  Validar duplicado ---
    all_data = load_all_payments()
    if str(payment_id) in all_data:
        return {"message": f"El pago {payment_id} ya existe."}

    # --- Registrar el pago ---
    save_payment(payment_id, amount, payment_method, STATUS_REGISTRADO)
    return {"message": f"Pago {payment_id} registrado con exito"}




# POST en el path /payments/{payment_id}/update que cambie los parametros de una pago (amount, payment_method)
@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float = None, payment_method: str = None, status: str = None):
    all_data = load_all_payments()

    # Verificamos si existe el payment_id
    if payment_id not in all_data:
        return {"error": f"Pago {payment_id} no encontrado"}

    data = load_payment(payment_id)

    if data[STATUS] == STATUS_REGISTRADO:
        if amount is not None:
            data[AMOUNT] = amount
        if payment_method is not None:
            data[PAYMENT_METHOD] = payment_method
        if status is not None:
            data[STATUS] = status

        save_payment_data(payment_id, data)
        return {"message": f"Pago {payment_id} actualizado"}
    else:
        return {"error": f"Pago {payment_id} no puede ser actualizado"}


# POST en el path /payments/{payment_id}/pay que intente.
@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    all_data = load_all_payments()

    # Verificamos si existe el payment_id
    if payment_id not in all_data:
        return {"error": f"Pago {payment_id} no encontrado"}

    data = load_payment(payment_id)

    if data[STATUS] == STATUS_REGISTRADO:
        if (data[PAYMENT_METHOD] == "paypal" and data[AMOUNT] < 5000):
            data[STATUS] = STATUS_PAGADO
            save_payment_data(payment_id, data)
            return {"message": f"Pago {payment_id} procesado"}

        if (data[PAYMENT_METHOD] == "creditCard" and data[AMOUNT] < 10000):
            q = sum(1 for payment in all_data.values() if payment[PAYMENT_METHOD] == "creditCard" and payment[STATUS] == STATUS_REGISTRADO)
        
            if q < 2:
                data[STATUS] = STATUS_PAGADO
                save_payment_data(payment_id, data)
                return {"message": f"Pago {payment_id} procesado"}
            else:
                data[STATUS] = STATUS_FALLIDO
                save_payment_data(payment_id, data)
                return {"message": f"Pago {payment_id} fallido por limite de pagos con tarjeta de crédito"}
        
        else:
            data[STATUS] = STATUS_FALLIDO
            save_payment_data(payment_id, data)
            return {"message": f"Pago {payment_id} fallido por excede el monto permitido"}
        
    else:
        return {"error": f"Pago {payment_id} no puede ser procesado"}
    

# POST en el path /payments/{payment_id}/revert que revertir el pago.
@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    
    all_data = load_all_payments()

    # Verificamos si existe el payment_id
    if payment_id not in all_data:
        return {"error": f"Pago {payment_id} no encontrado"}
    
    data = load_payment(payment_id)

    if data[STATUS] == STATUS_FALLIDO:
        data[STATUS] = STATUS_REGISTRADO
        save_payment_data(payment_id, data)
        return {"message": f"Pago {payment_id} revertido"}
    else:
        return {"error": f"Pago {payment_id} no puede ser revertido"}