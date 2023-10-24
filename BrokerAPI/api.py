from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from market_data import Session, Customer, Order, get_all_customers
from typing import List

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
    session = Session()
    try:
        # Create a new customer based on the provided data
        new_customer = Customer(name=customer.name, account_balance=customer.account_balance)
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)  # Refresh the object to get the generated ID

        return new_customer
    finally:
        session.close()
    pass

@app.post("/orders/")
def create_order(order: OrderCreate):
    # Implement order creation logic using data.py functions
    pass

# Create a route to add funds to a user's account
@app.post("/customers/add_funds/")
def add_funds(add_funds_data: AddFunds):
    session = Session()
    try:
        # Check if the customer with the given ID exists
        customer = session.query(Customer).filter(Customer.id == add_funds_data.customer_id).first()
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Update the customer's account balance by adding the specified amount
        customer.account_balance += add_funds_data.amount
        session.commit()
        return customer
    finally:
        session.close()

@app.get("/customers/")
def get_customers():
    customers = get_all_customers()
    return customers