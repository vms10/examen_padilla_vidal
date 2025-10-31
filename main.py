from fastapi import FastAPI
from routers import payments_router

app = FastAPI()

app.include_router(payments_router.router)