from fastapi import FastAPI
import uvicorn
from app.routes import user, product, cart, transaction
from app.services import auth

app = FastAPI()

app.include_router(auth.auth_router)
app.include_router(user.user_router)
app.include_router(product.product_router)
app.include_router(cart.cart_router)
app.include_router(transaction.transaction_router)