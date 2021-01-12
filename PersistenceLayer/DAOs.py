from PersistenceLayer.DTOs import Vaccines, Suppliers, Logistics, Clinics


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""Insert into vaccines(id, date, supplier, quantity) 
        Values(?, ?, ?, ?)""", [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM vaccines WHERE id = ?""", [vaccine_id])
        return Vaccines(*c.fetchone())

    def find_oldest_vaccine(self):
        c = self._conn.cursor()
        c.execute("""Select * from vaccines 
                    Where date = (Select MIN(date) from vaccines)""")
        return Vaccines(*c.fetchone())

    def update_vaccine_entry(self, amount, entry):
        self._conn.execute("""Update vaccines
                        Set quantity = quantity-? 
                        Where id = ?""", (amount, entry))

    def delete_entry(self, entry):
        self._conn.execute("""Delete from vaccines
                        Where id = ?""", entry)

    def amount(self):
        c = self._conn.cursor()
        c.execute("""Select amount from Vaccines""")
        return c.fetchall()


class _Suppliers:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""Insert into suppliers( id, name, logistic) 
        Values(?, ?, ?)""", [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM suppliers WHERE id = ?""", [supplier_id])
        return Suppliers(*c.fetchone())

    def find_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM suppliers WHERE name = ?""", [supplier_name])
        return Suppliers(*c.fetchone())


class _Logistics:

    def __init__(self, conn):
        self._conn = conn

    def insert_l(self, logistic):
        self._conn.execute("""Insert into logistics(id, name, count_sent, count_received) 
        Values(?, ?, ?, ?)""", [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM logistics WHERE id = ?""", [logistic_id])
        return Logistics(*c.fetchone())

    def update_sent(self, logistic_id, amount):
        self._conn.execute("""Update Logistics 
                    Set count_sent = count_sent+? Where id =?""", (amount, logistic_id))

    def update_received(self, logistic_id, amount):
        self._conn.execute("""Update Logistics 
                Set count_received = count_received+?
                Where Logistics.id = ?""", (amount, logistic_id))

    def sent_received(self):
        c = self._conn.cursor()
        c.execute("""Select count_sent, count_received
         from Clinics""")
        return c.fetchall()


class _Clinics:

    def __init__(self, conn):
        self._conn = conn

    def insert_c(self, clinic):
        self._conn.execute("""Insert into clinics(id, location, demand, logistic) 
        Values(?, ?, ?, ?)""", [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM clinics WHERE id = ?""", [clinic_id])
        return Clinics(*c.fetchone())

    def update(self, amount, location):
        self._conn.execute("""Update Clinics 
                Set demand = demand-?
                Where location=?""", (amount, location))

    def find_by_location(self, location):
        c = self._conn.cursor()
        c.execute("""Select * 
                           From Clinics Where location =?""", location)
        return Clinics(*c.fetchone())

    def demand(self):
        c = self._conn.cursor()
        c.execute("""Select demand from Clinics""")
        return c.fetchall()

