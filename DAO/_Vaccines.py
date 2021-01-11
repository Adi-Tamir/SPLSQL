from DTO.DTOs import Vaccines


def __init(self, conn):
    self._conn = conn


def insert(self, vaccine):
    self._conn.execute("""Insert into vaccines(id, date, supplier, quantity) 
    Values(?, ?, ?, ?)""", [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


def find(self, vaccine_id):
    c = self._conn.cursor()
    c.execute("""SELECT * FROM vaccines WHERE id = ?""", [vaccine_id])
    return Vaccines(*c.fetchone())

