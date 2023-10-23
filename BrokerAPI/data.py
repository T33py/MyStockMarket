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

def get_all_customers():
    session = Session()
    try:
        customers = session.query(Customer).all()
        return customers
    finally:
        session.close()

# Additional functions to interact with the database (e.g., inserting, updating, and querying data)
# You can add functions to add, update, and query customer data, buy/sell orders, etc.
