from DTO.DTOs import Logistics


class _Logistics:

    def __init(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""Insert into logistics(id, name, count_sent, count_received) 
        Values(?, ?, ?, ?)""", [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM logistics WHERE id = ?""", [logistic_id])
        return Logistics(*c.fetchone())

    def update(self, logistic_id, amount):
        self._conn.execute("""Update Logistics 
                Set count_received = count_received+?
                Where Logistics.id = ?""", (amount, logistic_id))
