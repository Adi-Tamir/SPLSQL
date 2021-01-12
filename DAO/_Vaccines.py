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
        c = self._conn.cursor()
        c.execute("""Select id, quantity from vaccines 
                    Where date = min(date)""")
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


