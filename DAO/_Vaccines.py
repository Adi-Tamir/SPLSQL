from DTO.DTOs import Vaccines


class _Vaccines:

    def __init(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""Insert into vaccines(id, date, supplier, quantity) 
        Values(?, ?, ?, ?)""", [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM vaccines WHERE id = ?""", [vaccine_id])
        return Vaccines(*c.fetchone())

    def find_oldest_vaccine(self):
        self._conn.execute("""Select id, quantity from Vaccines 
                    Where date = min(date)""")
        return Vaccines(*self._conn.fetchone())

    def update_vaccine_entry(self, amount, entry):
        self._conn.execute("""Update Vaccines
                        Set quantity = quantity-? 
                        Where id = ?""", (amount, entry))


