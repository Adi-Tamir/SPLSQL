from DTO.DTOs import Clinics


class _Clinics:

    def __init(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""Insert into clinics(id, location, demand, logistic) 
        Values(?, ?, ?)""", [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM clinics WHERE id = ?""", [clinic_id])
        return Clinics(*c.fetchone())

    def update(self, amount, location):
        self._conn.execute("""Update Clinics 
                Set demand = demand-?
                Where location=?""", (amount, location))
