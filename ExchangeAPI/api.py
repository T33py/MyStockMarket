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

class OrderExecution(BaseModel):
    order: int
    counterparty: int

class CreateStock(BaseModel):
    id: int
    stock_symbol: str
    company: str
    company_description: str
    price: float

#####################
# Create routes for managing customers and orders
#####################
@app.put("/customers/create/")
def create_customer(customer: CustomerCreate):
    new_customer = market_data.create_new_customer(name=customer.name, account_balance=customer.account_balance)
    if new_customer is None:
        raise HTTPException(409, 'User already exists')
    return new_customer


@app.put("/orders/create/")
def create_order(order: OrderCreate):
    new_order = market_data.create_new_order(customer_id=order.customer_id, order_type=order.order_type, stock_symbol=order.stock_symbol, quantity=order.quantity, price=order.price)
    
    if new_order is None:
        raise HTTPException(400, 'Failed to create order')
    return new_order


@app.put()
def create_stock(stock: CreateStock):
    new_stock = market_data.create_stock(id=stock.id, symbol=stock.stock_symbol, company=stock.company, company_description=stock.company_description, price=stock.price)
    if new_stock is None:
        raise HTTPException(400, 'Failed to create stock')
    return new_stock


@app.post("/orders/execute/")
def execute_order(exec: OrderExecution):
    executed_order = market_data.execute_order(order=exec.order, counterparty=exec.counterparty)
    if executed_order is None:
        raise HTTPException(400, 'Failed to execute order')
    return executed_order


# Create a route to add funds to a user's account
@app.post("/customers/change_funds/")
def change_funds(add_funds_data: AddFunds):
    if market_data.change_account_balance(id=add_funds_data.customer_id, change=add_funds_data.amount):
        return { "message": "Funds deposited" }
    else:
        raise HTTPException(409, 'UserID not found')


@app.get("/customers/")
def get_customers():
    customers = market_data.get_all_customers()
    return customers
