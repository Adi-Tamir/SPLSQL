

def send_shipment(conn, location, amount):
    cur = conn.cursor()
    cur.execute("""Update Clinics 
    Set demand = demand-?
    Where location=?""", (amount, location))
    while amount > 0:
        cur.execute("""Select id, quantity from Vaccines 
        Where date = min(date)""")
        entry = cur.fetchone()
        quantity = cur.fetchone()
        if quantity > amount:
            cur.execute("""Update Vaccines
            Set amount = amount-? 
            Where id = ?""", (quantity, entry))
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


