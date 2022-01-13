# file: persistence.py

import sqlite3
import atexit


# Data Transfer Objects:
class Hat(object):
    def __init__(self, id, topping, supplier_id, quantity):
        self.id = id
        self.topping = topping
        self.supplier_id = supplier_id
        self.quantity = quantity


class Supplier(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Order(object):
    def __init__(self, id, location, hat_id):
        self.id = id
        self.location = location
        self.hat_id = hat_id


# Data Access Objects:
# All of these are meant to be singletons
class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("""
               INSERT INTO hats (id, topping, supplier_id, quantity) VALUES (?, ?, ?, ?)
           """, [hat.id, hat.topping , hat.supplier_id, hat.quantity])

    def find(self, hat_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, topping, supplier_id, quantity FROM hats WHERE id = ?
        """, [hat_id])

        return Hat(*c.fetchone())


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name) VALUES (?, ?)
        """, [supplier.id, supplier.name])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT id,name FROM suppliers WHERE id = ?
            """, [id])

        return Supplier(*c.fetchone())


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("""
            INSERT INTO orders (id, location, hat_id) VALUES (?, ?, ?)
        """, [order.id, order.location, order.hat_id])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT id,location, hat_id FROM orders WHERE id = ?
            """, [id])

        return Order(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, location, hat_id FROM orders
        """).fetchall()

        return [Order(*row) for row in all]


# The Repository
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('grades.db')
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):

        self._conn.executescript("""
            CREATE TABLE hats (
                id      INT         PRIMARY KEY,
                name    TEXT        NOT NULL
            );

            CREATE TABLE suppliers (
                num                 INT     PRIMARY KEY,
                expected_output     TEXT    NOT NULL
            );

            CREATE TABLE orders (
                student_id      INT     NOT NULL,
                assignment_num  INT     NOT NULL,
                grade           INT     NOT NULL,

                FOREIGN KEY(student_id)     REFERENCES students(id),
                FOREIGN KEY(assignment_num) REFERENCES assignments(num),

                PRIMARY KEY (student_id, assignment_num)
            );
        """)


# the repository singleton
repo = _Repository()
atexit.register(repo._close)