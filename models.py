from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# ================= user model ========================
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(40), index=True, unique=True)
    balance = Column(Float)
    phone = Column(String(25), index=True, unique=True)
    currency = Column(String(6)) 
    full_name = Column(String(60))
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)                      # for first database entry, Immutable 
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)    # subsequent updates and changes in database info and last account usage times



# ======================transaction model ========================

class Transaction(Base):
    __tablename__ = "transactions"
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    receiver_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float)
    transaction_id = Column(String(60), primary_key=True, index=True)
    transaction_type = Column(String(15)) # eg, deposit, withdrawal, transfer etc
    currency = Column(String(6))
    initial_balance = Column(Float)
    remaining_balance = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String)                                     # eg. pending, completed, failed, blocked, sent,  restricted etc
    payment_method = Column(String, index=True) # eg, mastercard, account, visa card etc. --NOTE: not really sure about this whether I should index it 
    sender = relationship(User, foreign_keys=[sender_id])   
    receiver = relationship(User, foreign_keys=[receiver_id])