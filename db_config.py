from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "sms_inventory"
DB_PATH = os.path.join("/data", "inventory.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(bind=engine)


# engine = create_engine(
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4",
#     echo=False
# )

# SessionLocal = sessionmaker(bind=engine)
