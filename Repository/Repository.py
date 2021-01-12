import atexit
import sqlite3
from DAO import _Vaccines, _Suppliers, _Logistics, _Clinics
from DTO.DTOs import Logistics, Clinics, Suppliers, Vaccines


class Repository:

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_database(self):
        self._conn.executescript("""
        CREATE TABLE vaccines(
            id INT PRIMARY KEY autoincrement,
            date DATETIME NOT NULL
            supplier INT NOT NULL,
            quantity INT NOT NULL,
            FOREIGN KEY (supplier) REFERENCES Suppliers(id)
        );
    
        CREATE TABLE suppliers(
            id INT PRIMARY KEY autoincrement,
            name TEXT NOT NULL
            FOREIGN KEY (logistic) REFERENCES Logistics(id)
        );
    
         CREATE TABLE clinics(
            id INT PRIMARY KEY autoincrement,
            location TEXT NOT NULL
            demand INT NOT NULL,
            FOREIGN KEY (logistic) REFERENCES Logistics(id)
        );
    
        CREATE TABLE logistics(
            id INT PRIMARY KEY autoincrement,
            name TEXT NOT NULL
            count_sent INT NOT NULL,
            count_received INT NOT NULL,
        );
            """)
        pass

    def insert_info(self, config_path):
        with open(config_path) as f:
            lines = f.readlines()
        nums_line = lines[0]
        nums = nums_line.split(",")

        end = len(lines) - 1
        start = end - nums[3] + 1
        for line in range(start, end):
            logistic = self.create_logistics(self, lines[line])
            _Logistics.insert(logistic)

        end -= 1
        start = end - nums[2] + 1
        for line in range(start, end):
            clinic = self.create_clinics(self, lines[line])
            _Clinics.insert(clinic)

        end -= 1
        start = end - nums[1] + 1
        for line in range(start, end):
            supplier = self.create_supplier(self, lines[line])
            _Suppliers.insert(supplier)

        end -= 1
        start = end - nums[0] + 1
        for line in range(start, end):
            vaccine = self.create_vaccines(self, lines[line])
            _Vaccines.insert(vaccine)
        pass

    def create_logistics(self, line):
        args = line.split(",")
        logistic = Logistics(args[0], args[1], args[2], args[3])
        return logistic

    def create_clinics(self, line):
        args = line.split(",")
        clinic = Clinics(args[0], args[1], args[2], args[3])
        return clinic

    def create_supplier(self, line):
        args = line.split(",")
        supplier = Suppliers(args[0], args[1], args[2])
        return supplier

    def create_vaccines(self, line):
        args = line.split(",")
        vaccine = Vaccines(args[0], args[1], args[2], args[3])
        return vaccine

    def complete_orders(self, orders_path, output_path):
        with open(orders_path) as f:
            lines = f.readlines()
        for line in lines:
            par = line.split(',')
            if len(par) == 3:
                self.receive_shipment(self, par[0], par[1], par[2])
            else:
                send_shipment(par[0], par[1])
            order = get_order_results()
            f = open(output_path, "a")
            f.write(order + '\n')
            f.close()
        pass

    def receive_shipment(self, name, amount, date):
        supplier = _Suppliers.find_by_name(name)
        vaccine = Vaccines(date, supplier.name, amount)
        _Vaccines.insert(vaccine)
        _Logistics.update(supplier.logistic, amount)
        pass

    def send_shipment(self, location, amount):
        _Clinics.update(amount, location)
        while amount > 0:
            vaccine_entry = _Vaccines.find_oldest_vaccine()
            if vaccine_entry.quantity > amount:
                _Vaccines.update_vaccine_entry(amount, vaccine_entry.id)
                cur.execute("""Select logistic 
                From Clinics Where location =?""", location)
                logistic_id = cur.fetchone()
                cur.execute("""Update Logistics 
                Set count_sent = count_sent+?
                Where id =?""", (amount, logistic_id))
                amount = 0
            else:
                amount -= quantity
                cur.execute("""Delete from Vaccines
                Where id = ?""", entry)
                cur.execute("""Select logistic 
                            From Clinics Where location =?""", location)
                logistic_id = cur.fetchone()
                cur.execute("""Update Logistics 
                            Set count_sent = count_sent+?
                            Where id =?""", (quantity, logistic_id))
        pass
# the repository singleton
repo = Repository()
atexit.register(repo._close)


