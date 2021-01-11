from DTO.DTOs import Suppliers


def __init(self, conn):
    self._conn = conn


def insert(self, supplier):
    self._conn.execute("""Insert into suppliers( id, name, logistic) 
    Values(?, ?, ?)""", [supplier.id, supplier.name, supplier.logistic])


def find(self, supplier_id):
    c = self._conn.cursor()
    c.execute("""SELECT * FROM suppliers WHERE id = ?""", [supplier_id])
    return Suppliers(*c.fetchone())

