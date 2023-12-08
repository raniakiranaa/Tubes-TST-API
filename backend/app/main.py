from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, product, cart, transaction, recommendations
from app.utils import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.auth_router)
app.include_router(user.user_router)
app.include_router(product.product_router)
app.include_router(cart.cart_router)
app.include_router(transaction.transaction_router)
app.include_router(recommendations.rec_router)