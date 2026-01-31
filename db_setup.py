import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# -------------------------
# CHANGE THESE VALUES
# -------------------------
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "sms_inventory"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
    echo=True
)

Base = declarative_base()

# -------------------------
# Tables
# -------------------------
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    cupboard = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    emp_id = Column(String(20), primary_key=True)
    emp_name = Column(String(255), nullable=False)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=datetime.now)
    item_id = Column(Integer)
    transaction_type = Column(String(10))
    qty = Column(Integer)
    taken_by = Column(String(20))
    given_by = Column(String(20))
    balance_after = Column(Integer)

# -------------------------
# Create tables
# -------------------------
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# -------------------------
# Load Excel
# -------------------------
df = pd.read_excel("Inventoryy.xlsx")

df.columns = [c.strip() for c in df.columns]

for _, row in df.iterrows():
    item = Inventory(
        item_name=str(row["Material"]).strip(),
        cupboard=str(row["Description"]).strip(),
        quantity=int(row["Quantity"])
    )
    session.add(item)

session.commit()

print("✅ Inventory imported into MySQL successfully")
