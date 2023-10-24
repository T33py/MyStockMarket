from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import market_data

app = FastAPI()

#####################
# Define Pydantic models for request and response data
#####################
class CustomerCreate(BaseModel):
    name: str
    account_balance: float

class OrderCreate(BaseModel):
    customer_id: int
    order_type: str
    stock_symbol: str
    quantity: int
    price: float

class AddFunds(BaseModel):
    customer_id: int
    amount: float


#####################
# Create routes for managing customers and orders
#####################
@app.post("/customers/create/")
def create_customer(customer: CustomerCreate):
    new_customer = market_data.create_new_customer(name=customer.name, account_balance=customer.account_balance)
    if new_customer is None:
        raise HTTPException(409, 'User already exists')
    return new_customer

@app.post("/orders/")
def create_order(order: OrderCreate):
    # Implement order creation logic using data.py functions
    pass

# Create a route to add funds to a user's account
@app.post("/customers/change_funds/")
def change_funds(add_funds_data: AddFunds):
    if market_data.change_account_balance(add_funds_data.customer_id, add_funds_data.amount):
        return { "message": "Funds deposited" }
    else:
        raise HTTPException(409, 'UserID not found')

@app.get("/customers/")
def get_customers():
    customers = market_data.get_all_customers()
    return customers