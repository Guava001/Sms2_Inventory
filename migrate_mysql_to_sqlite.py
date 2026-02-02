from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_config import Base
from models import Inventory, TransactionLog
from db_config import Base, MySQLSession, SQLiteSession


# MySQL engine (OLD)
mysql_engine = create_engine(
    "mysql+pymysql://USER:PASSWORD@HOST/DBNAME"
)

# SQLite engine (NEW)
sqlite_engine = create_engine(
    "sqlite:///data.db",
    connect_args={"check_same_thread": False}
)

MySQLSession = sessionmaker(bind=mysql_engine)
SQLiteSession = sessionmaker(bind=sqlite_engine)

Base.metadata.create_all(sqlite_engine)

mysql_session = MySQLSession()
sqlite_session = SQLiteSession()

items = mysql_session.query(Inventory).all()

for item in items:
    sqlite_session.add(Inventory(
        name=item.name,
        quantity=item.quantity,
        cupboard=item.cupboard
    ))

sqlite_session.commit()

mysql_session.close()
sqlite_session.close()

print("Migration completed")
