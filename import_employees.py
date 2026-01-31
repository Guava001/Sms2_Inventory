import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String

DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "sms_inventory"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(String(20), primary_key=True)
    emp_name = Column(String(255))

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel("employees.xlsx")

# Clear existing employees
session.query(Employee).delete()
session.commit()

for _, row in df.iterrows():
    emp = Employee(
        emp_id=str(row["Emp_ID"]).strip(),
        emp_name=str(row["Emp_Name"]).strip()
    )
    session.add(emp)

session.commit()
session.close()

print("✅ Employees imported successfully")
