from flask import Flask, render_template, request, redirect
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from flask import request, redirect, flash
from db_config import SessionLocal, engine
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = "sms_inventory_secret_key_123"
Base = declarative_base()

# ------------------ MODELS ------------------

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(255))
    cupboard = Column(String(100))
    quantity = Column(Integer)

class Employee(Base):
    __tablename__ = "employees"
    emp_id = Column(String(20), primary_key=True)
    emp_name = Column(String(255))


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=datetime.now)
    item_id = Column(Integer)
    transaction_type = Column(String(10))
    qty = Column(Integer)
    taken_by = Column(String(20))
    given_by = Column(String(20))
    balance_after = Column(Integer)

# ------------------ ROUTES ------------------

@app.route("/", methods=["GET", "POST"])
def index():
    session = SessionLocal()

    if request.method == "POST":

        item_id = int(request.form["item_id"])
        action = request.form["action"]
        qty = int(request.form["qty"])
        taken_by = request.form.get("taken_by", "").strip()

        # 1️⃣ Taken By mandatory
        if not taken_by:
            flash("Taken By (Employee ID) is mandatory", "danger")
            session.close()
            return redirect("/")

        # 2️⃣ Employee MUST exist
        emp = session.query(Employee).filter(Employee.emp_id == taken_by).first()
        if not emp:
            flash("Invalid Employee ID", "danger")
            session.close()
            return redirect("/")

        # 3️⃣ Item must exist
        item = session.query(Inventory).filter(Inventory.id == item_id).first()
        if not item:
            flash("Invalid item selected", "danger")
            session.close()
            return redirect("/")

        # 4️⃣ Stock validation
        if action == "OUT" and item.quantity < qty:
            flash("Not enough stock available", "danger")
            session.close()
            return redirect("/")

        # 5️⃣ Update inventory
        if action == "OUT":
            item.quantity -= qty
        else:
            item.quantity += qty

        # 6️⃣ Record transaction
        txn = Transaction(
            date_time=datetime.now(),
            item_id=item.id,
            transaction_type=action,
            qty=qty,
            taken_by=taken_by,
            balance_after=item.quantity
        )

        session.add(txn)
        session.commit()

        flash("Transaction successful", "success")
        return redirect("/")


        session.close()

        flash("Transaction successful", "success")
        return redirect("/")

    items = session.query(Inventory).all()
    session.close()
    return render_template("index.html", items=items)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     session = SessionLocal()

#     if request.method == "POST":
#         item_id = int(request.form["item_id"])
#         action = request.form["action"]
#         qty = int(request.form["qty"])
#         taken_by = request.form["taken_by"]

#         if not taken_by:
#             flash("Taken By (Employee ID) is mandatory", "danger")
#             return redirect("/")
#         # given_by = request.form["given_by"]

#         item = session.query(Inventory).filter(Inventory.id == item_id).first()

#         if action == "OUT" and qty > item.quantity:
#             return "ERROR: Not enough stock"

#         if action == "OUT":
#             item.quantity -= qty
#         else:
#             item.quantity += qty

#         txn = Transaction(
#             item_id=item.id,
#             transaction_type=action,
#             qty=qty,
#             taken_by=taken_by,
#             # given_by=given_by,
#             balance_after=item.quantity
#         )

#         session.add(txn)
#         session.commit()
#         session.close()

#         return redirect("/")

#     items = session.query(Inventory).all()
#     session.close()

#     return render_template("index.html", items=items)

from flask import jsonify

@app.route("/get_item/<int:item_id>")
def get_item(item_id):
    print("GET ITEM CALLED:", item_id)

    session = SessionLocal()   # ✅ CREATE SESSION

    item = session.query(Inventory).filter(
        Inventory.id == item_id
    ).first()

    session.close()            # ✅ CLOSE SESSION

    if not item:
        return jsonify({"error": "Item not found"})

    return jsonify({
        "quantity": item.quantity,
        "cupboard": item.cupboard
    })

@app.route("/get_employee/<emp_id>")
def get_employee(emp_id):
    session = SessionLocal()
    emp = session.query(Employee).filter(Employee.emp_id == emp_id).first()
    session.close()

    if not emp:
        return {"name": ""}   # silent failure for typing

    return {"name": emp.emp_name}


# @app.route("/get_employee/<emp_id>")
# def get_employee(emp_id):
#     session = SessionLocal()
#     emp = session.query(Employee).filter(Employee.emp_id == emp_id).first()

#     if not emp:
#         flash("Invalid Employee ID", "danger")
#         return redirect("/")

#     session.close()

#     if emp:
#         return {"name": emp.emp_name}
#     return {"name": ""}


@app.route("/transactions")
def transactions_log():
    session = SessionLocal()

    logs = (
        session.query(
            Transaction.date_time,
            Inventory.item_name,
            Transaction.transaction_type,
            Transaction.qty,
            Employee.emp_name,
            Transaction.balance_after
        )
        .join(Inventory, Transaction.item_id == Inventory.id)
        .outerjoin(Employee, Transaction.taken_by == Employee.emp_id)
        .order_by(Transaction.date_time.desc())
        .all()
    )

    session.close()

    return render_template("transactions.html", logs=logs)


# ------------------

if __name__ == "__main__":
    app.run(debug=True)
