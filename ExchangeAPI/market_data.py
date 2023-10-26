# data.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from consts import ordertypes, orderstatuses

# Create a SQLAlchemy database engine
DATABASE_URL = "sqlite:///exchange.db"
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
    customer_id = Column(Integer, ForeignKey('customers.id'), index=True)
    stock_symbol = Column(String, ForeignKey('stocks.symbol'), index=True)
    number_of_shares = Column(Integer)
    bought_at_price = Column(Float)
    bought_at_date = Column(String)

class Stock(Base):
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True, index=True)
    stock_symbol = Column(String, index=True)
    company = Column(String, index=True)
    company_description = Column(String)
    price = Column(Float, index=True)


# Define the SQLAlchemy model for buy and sell orders
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), index=True)
    order_type = Column(String)  # 'buy' or 'sell'
    stock_symbol = Column(String, ForeignKey('stocks.symbol'), index=True)
    quantity = Column(Integer)
    price = Column(Float)
    status = Column(String)

Base.metadata.create_all(bind=engine)


def get_all_customers()-> list[Customer]:
    session = Session()
    try:
        customers = session.query(Customer).all()
        return customers
    finally:
        session.close()


def create_new_order(customer_id: int, order_type: String, stock_symbol: String, quantity: int, price: float)-> Order|None:
    '''
    Create a new order in the market
    '''
    session = Session()
    new_order = Order(
        customer=customer_id, 
        order_type=order_type, 
        stock_symbol=stock_symbol, 
        quantity=quantity, price=price, 
        status=orderstatuses.ACTIVE
        )
    try:
        session.add(new_order)
        session.commit()
        session.refresh(new_order) # get order ID
        return new_order
    except:
        new_order = None
    finally:
        session.close()
    return new_order

def get_orders(stock_symbol)-> list[Order]:
    session = Session()
    try:
        return session.query(Order).filter(Order.stock_symbol == stock_symbol).all()
    finally:
        session.close()
    return None

def execute_order(order: int, counterparty: int)-> Order|None:
    '''
    Execute the provided order with the customer id provided as counterparty.
    This will only execute ACTIVE orders, and returns the order if successful, otherwise None.
    TODO: implement something to indicate why stuff failed
    '''
    session = Session()
    try:
        # is the order in the correct state?
        order = session.query(Order).filter(Order.id).first()
        if order is None:
            return None
        if order.status != orderstatuses.ACTIVE:
            return None
        
        # does the buyer have the funds?
        buyer_account = session.query(Customer).filter(Customer.id == buyer.id).first()
        seller_account = session.query(Customer).filter(Customer.id == counterparty).first()
        total = order.price * order.quantity
        if buyer_account is None or seller_account is None:
            return None
        if buyer_account.account_balance < total:
            return None
        
        # does the seller hold the position?
        seller = None
        buyer = None
        create_buyer = False
        if order.order_type == ordertypes.BUY:
            seller = session.query(Position).filter(Position.customer_id == counterparty and Position.stock_symbol == order.stock_symbol).first()
            buyer = session.query(Position).filter(Position.customer_id == order.customer_id).first()
            if buyer is None:
                buyer = Position(customer_id=order.customer_id, stock_symbol=order.stock_symbol, quantity=order.quantity, bought_at_price=order.price, bought_at_date='2000-12-31')
                create_buyer = True
        else: # it is a sell order
            buyer = session.query(Position).filter(Position.customer_id == counterparty).first()
            seller = session.query(Position).filter(Position.customer_id == order.customer_id and Position.stock_symbol == order.stock_symbol).first()
            if buyer is None:
                buyer = Position(customer_id=counterparty, stock_symbol=order.stock_symbol, quantity=order.quantity, bought_at_price=order.price, bought_at_date='2000-12-31')
                create_buyer = True

        if seller is None:
            return None
        
        # update the positions
        buyer_account.account_balance -= total
        seller_account += total

        if create_buyer:
            session.add(buyer)
        else:
            pr_qty = buyer.number_of_shares
            pr_avg = buyer.bought_at_price
            buyer.number_of_shares += order.quantity
            buyer.bought_at_price = (pr_qty * pr_avg + total)/buyer.number_of_shares

        seller.number_of_shares -= order.quantity

        # update the stock
        stock = session.query(Stock).filter(Stock.stock_symbol == order.stock_symbol).first()
        if stock is not None:
            stock.price = order.price

        # update the order and commit
        order.status = orderstatuses.CLOSED
        session.commit()
        session.refresh(buyer)
        return order
    finally:
        session.close()
    return None


def create_new_customer(name: String, account_balance: Float)-> Customer|None:
    '''
    Create a customer with a name that is not currently in use.
    name: name to try and create a user with
    account_balance: initial balance of the account
    '''
    session = Session()
    new_customer = Customer(
        name=name, 
        account_balance=account_balance)
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
    except:
        return False
    finally:
        session.close()

    return True

def create_stock(id, symbol, company, company_description, price):
    session = Session()
    try:
        new_stock = Stock(id=id, stock_symbol=symbol, company=company, company_description=company_description, price=price)
        session.add(new_stock)
        return new_stock
    finally:
        session.close()
    return None