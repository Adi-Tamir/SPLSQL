

def receive_shipment(conn, name, amount, date):
    cur = conn.cursor()
    cur.execute("""Insert into Vaccines(id, date, supplier, quantity)'
                Values(?, ?, ?, ?)""", (date, name, amount))
    cur.execute("""Select logistic from Suppliers 
    Where Suppliers.name = ?""", name)
    logistic_id = cur.fetchone()
    cur.execute("""Update Logistics 
    Set count_received = count_received+?
    Where Logistics.id = ?""", (amount, logistic_id))
    conn.commit()
    #Write to file
    pass
