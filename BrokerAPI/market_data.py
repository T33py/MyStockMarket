# data.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy database engine
DATABASE_URL = "sqlite:///stockbroker.db"
engine = create_engine(DATABASE_URL)

# Create a Session class to interact with the database
Session = sessionmaker(bind=engine)

# Define the SQLAlchemy model for customer data
Base = declarative_base()
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    account_balance = Column(Float)

# Define the SQLAlchemy model for positions
class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    stock_symbol = Column(String, index=True)
    number_of_shares = Column(Integer)
    bought_at_price = Column(Float)
    bought_at_date = Column(String)

class Stock(Base):
    __tablename__ = 'Stocks'
    
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)
    company = Column(String, index=True)
    company_description = Column(String)
    price = Column(Float, index=True)


# Define the SQLAlchemy model for buy and sell orders
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    order_type = Column(String)  # 'buy' or 'sell'
    stock_symbol = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

Base.metadata.create_all(bind=engine)


def get_all_customers()-> list[Customer]:
    session = Session()
    try:
        customers = session.query(Customer).all()
        return customers
    finally:
        session.close()


def create_new_customer(name: String, account_balance: Float)-> Customer|None:
    '''
    Create a customer with a name that is not currently in use.
    name: name to try and create a user with
    account_balance: initial balance of the account
    '''
    session = Session()
    new_customer = Customer(name=name, account_balance=account_balance)
    try:
        # Create a new customer based on the provided data
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)  # Refresh the object to get the generated ID
    except:
        new_customer = None
    finally:
        session.close()
    
    return new_customer



def change_account_balance(id: int, change: Float)-> bool:
    '''
    Change the balance of the account with the provided id
    id: The id of the user whose account_balance is being changed
    change: Ammount to change account_balance by
    '''
    session = Session()
    try:
        # Check if the customer with the given ID exists
        customer = session.query(Customer).filter(Customer.id == id).first()
        if customer is None:
            return False

        # Update the customer's account balance by adding the specified amount
        customer.account_balance += change
        session.commit()
    finally:
        session.close()

    return True