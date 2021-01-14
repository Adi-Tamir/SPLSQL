import atexit
import sqlite3
from PersistenceLayer.DAOs import _Vaccines, _Logistics, _Clinics, _Suppliers

from PersistenceLayer.DTOs import Logistics, Clinics, Suppliers, Vaccines


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
    id INTEGER PRIMARY KEY autoincrement,
    date date NOT NULL,
    supplier INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (supplier) REFERENCES Suppliers(id)
);

CREATE TABLE suppliers(
    id INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
logistic INTEGER,
    FOREIGN KEY (logistic) REFERENCES Logistics(id)
);

 CREATE TABLE clinics(
    id INTEGER PRIMARY KEY autoincrement,
    location TEXT NOT NULL,
    demand INTEGER NOT NULL,
logistic INTEGER,
    FOREIGN KEY (logistic) REFERENCES Logistics(id)
);

CREATE TABLE logistics(
    id INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
    count_sent INTEGER NOT NULL,
    count_received INT NOT NULL
);
            """)
        #self._conn.commit()
        pass

    def commit(self):
        self._conn.commit()

    def insert_info1(self, config_path):
        with open(config_path) as f:
            lines = f.readlines()
        nums_line = lines[0]
        nums = nums_line.replace('\n', '').split(",")

        end = len(lines) - 1
        start = end - int(nums[3]) + 1
        for line in range(start, end + 1):
            logistic = self.create_logistics(lines[line].replace('\n', ''))
            _Logistics.insert_l(self, logistic)

        end = start - 1
        start = end - int(nums[2]) + 1
        for line in range(start, end + 1):
            clinic = self.create_clinics(lines[line].replace('\n', ''))
            _Clinics.insert_c(self, clinic)

        end = start - 1
        start = end - int(nums[1]) + 1
        for line in range(start, end + 1):
            supplier = self.create_supplier(lines[line].replace('\n', ''))
            _Suppliers.insert(self, supplier)

        end = start - 1
        start = end - int(nums[0]) + 1
        for line in range(start, end + 1):
            vaccine = self.create_vaccines(lines[line].replace('\n', ''))
            _Vaccines.insert(self, vaccine)
        self._conn.commit()
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

    def complete_orders1(self, orders_path, output_path):
        with open(orders_path) as f:
            lines = f.readlines()
        for line in lines:
            par = line.split(',')
            if len(par) == 3:
                self.receive_shipment(par[0], par[1], par[2])
            else:
                self.send_shipment(par[0], par[1])
            order = self.get_order_results()
            f = open(output_path, "a")
            f.write(order + '\n')
            f.close()
        self._conn.commit()
        pass

    def receive_shipment1(self, name, amount, date):
        next_id = int(self.vaccines.get_max_id()[0]) + 1
        supplier = self.suppliers.find_by_name(name)
        vaccine = Vaccines(next_id, date, supplier.name, amount)
        self.vaccines.insert(vaccine)
        self.logistics.update_received(supplier.logistic, amount)
        pass

    def send_shipment1(self, location, amount):
        _Clinics.update(self, amount, location)
        amount = int(amount)
        while int(amount) > 0:
            vaccine_entry = _Vaccines.find_oldest_vaccine(self)
            if int(vaccine_entry.quantity) > int(amount):
                self.vaccines.update_vaccine_entry(amount, vaccine_entry.id)
                logistic_id = self.clinics.find_by_location(location).logistic
                self.logistics.update_sent(logistic_id, amount)
                amount = 0
            else:
                amount -= vaccine_entry.quantity
                self.vaccines.delete_entry((vaccine_entry.id,))
                logistic_id = self.clinics.find_by_location(location).logistic
                self.logistics.update_sent(logistic_id, vaccine_entry.quantity)
        pass

    def get_order_results1(self):
        total_inventory = 0
        total_demand = 0
        total_received = 0
        total_sent = 0
        result = self.vaccines.amount()
        for row in result:
            total_inventory += row[0]
        result = self.clinics.demand()
        for row in result:
            total_demand += row[0]
        result = self.logistics.sent_received()
        for row in result:
            total_sent += row[0]
            total_received += row[1]
        result = str(total_inventory) + "," + str(total_demand) + "," + str(total_received) + "," + str(total_sent)
        return result


# the repository singleton
repo = Repository()
atexit.register(repo._close)


