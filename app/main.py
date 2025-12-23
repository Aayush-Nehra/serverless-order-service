from fastapi import FastAPI, HTTPException
from mangum import Mangum
from app.schemas import OrderCreate, OrderResponse
from app.repository import OrderRepository

app = FastAPI(title="Order Processing Service")
repo = OrderRepository()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate):
    created = repo.create_order(order)
    return created

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = repo.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

handler = Mangum(app)
