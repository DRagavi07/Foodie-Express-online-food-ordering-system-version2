
import sqlite3

# DATABASE CONNECTION
db = sqlite3.connect("onlinerest.db", check_same_thread=False)
db.execute("PRAGMA foreign_keys = ON")
mc = db.cursor()


# CREATE USERS TABLE
mc.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    password TEXT,
    address TEXT,
    phonenumber TEXT
)
""")


# CREATE ORDERS TABLE
mc.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    ordertotal REAL,
    paymentmethod TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
)
""")


# CREATE ORDER ITEMS TABLE
mc.execute("""
CREATE TABLE IF NOT EXISTS orderitems (
    order_id INTEGER,
    item_name TEXT,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)
""")


# ADD ORDER STATUS COLUMN IF NOT EXISTS
mc.execute("PRAGMA table_info(orders)")
columns = [column[1] for column in mc.fetchall()]

if "order_status" not in columns:
    mc.execute("""
        ALTER TABLE orders
        ADD COLUMN order_status TEXT DEFAULT 'Pending'
    """)

db.commit()


# USER LOGIN
def login(email, password):
    mc.execute(
        "SELECT password FROM users WHERE email = ?",
        (email,)
    )
    detail = mc.fetchone()

    if detail and detail[0] == password:
        return True

    return False


# USER SIGNUP
def signup(email, name, address, phnumber, sign_password):
    try:
        mc.execute("""
            INSERT INTO users
            (email, name, password, address, phonenumber)
            VALUES (?, ?, ?, ?, ?)
        """, (email, name, sign_password, address, phnumber))

        db.commit()
        return True

    except sqlite3.IntegrityError:
        db.rollback()
        return False


# GET USER DETAILS
def get_details(email):
    mc.execute("""
        SELECT user_id, name, address, phonenumber, email
        FROM users
        WHERE email = ?
    """, (email,))

    details = mc.fetchone()

    if details:
        return list(details)

    return None


# PLACE FOOD ORDER
def place_order(user_id, total_amt, paymentmethod, food_list, qty_list):
    try:
        mc.execute("""
            INSERT INTO orders
            (user_id, ordertotal, paymentmethod)
            VALUES (?, ?, ?)
        """, (user_id, total_amt, paymentmethod))

        order_id = mc.lastrowid

        for food, qty in zip(food_list, qty_list):
            mc.execute("""
                INSERT INTO orderitems
                (order_id, item_name, quantity)
                VALUES (?, ?, ?)
            """, (order_id, food, qty))

        db.commit()
        return True

    except Exception:
        db.rollback()
        return False


# GET ALL USER DATA
def get_user_data():
    mc.execute("""
        SELECT user_id, email, name, address, phonenumber
        FROM users
    """)

    details = mc.fetchall()

    return {
        'User Id': [i[0] for i in details],
        'Email Id': [i[1] for i in details],
        'Name': [i[2] for i in details],
        'Address': [i[3] for i in details],
        'Phone Number': [i[4] for i in details]
    }


# GET ALL ORDER DATA
def get_order_data():
    mc.execute("""
        SELECT order_id, user_id, ordertotal,
               paymentmethod, order_status
        FROM orders
    """)

    details = mc.fetchall()

    return {
        'Order Id': [i[0] for i in details],
        'User Id': [i[1] for i in details],
        'Total Amount': [i[2] for i in details],
        'Payment Method': [i[3] for i in details],
        'Order Status': [i[4] for i in details]
    }


# GET ALL ORDER ITEMS
def get_orderitem_data():
    mc.execute("SELECT * FROM orderitems")
    details = mc.fetchall()

    return {
        'Order ID': [i[0] for i in details],
        'Food Item': [i[1] for i in details],
        'Quantity': [i[2] for i in details]
    }


# UPDATE USER DETAILS
def update_details(user_id, email, name, address, number):
    mc.execute("""
        UPDATE users
        SET email = ?, name = ?, address = ?, phonenumber = ?
        WHERE user_id = ?
    """, (email, name, address, number, user_id))

    db.commit()
    return True


# UPDATE USER PASSWORD
def update_password(user_id, password):
    mc.execute("""
        UPDATE users
        SET password = ?
        WHERE user_id = ?
    """, (password, user_id))

    db.commit()
    return True


# GET PARTICULAR ORDER ITEMS
def get_orderitem_detail(order_id):
    mc.execute("""
        SELECT order_id, item_name, quantity
        FROM orderitems
        WHERE order_id = ?
    """, (order_id,))

    details = mc.fetchall()

    return {
        'Order ID': [i[0] for i in details],
        'Food Item': [i[1] for i in details],
        'Quantity': [i[2] for i in details]
    }


# DELETE USER
def delete_user(user_id):
    mc.execute(
        "DELETE FROM users WHERE user_id = ?",
        (user_id,)
    )

    db.commit()
    return True


# GET CUSTOMER ORDER HISTORY
def get_user_order_history(user_id):
    mc.execute("""
        SELECT
            o.order_id,
            oi.item_name,
            oi.quantity,
            o.ordertotal,
            o.paymentmethod,
            o.order_status
        FROM orders o
        JOIN orderitems oi
        ON o.order_id = oi.order_id
        WHERE o.user_id = ?
        ORDER BY o.order_id DESC
    """, (user_id,))

    details = mc.fetchall()

    return {
        'Order ID': [i[0] for i in details],
        'Food Item': [i[1] for i in details],
        'Quantity': [i[2] for i in details],
        'Total Amount': [i[3] for i in details],
        'Payment Method': [i[4] for i in details],
        'Order Status': [i[5] for i in details]
    }


# UPDATE ORDER STATUS
def update_order_status(order_id, status):
    mc.execute("""
        UPDATE orders
        SET order_status = ?
        WHERE order_id = ?
    """, (status, order_id))

    db.commit()

    return mc.rowcount > 0
