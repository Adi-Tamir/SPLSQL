
def get_order_results(conn):
    cur = conn.cursor()
    total_inventory = 0
    total_demand = 0
    total_received = 0
    total_sent = 0
    cur.execute("""Select amount from Vaccines""")
    result = cur.fetchall()
    for row in result:
        total_inventory += row[0]
    cur.execute("""Select demand from Clinics""")
    result = cur.fetchall()
    for row in result:
        total_demand += row[0]
    cur.execute("""Select count_sent, count_received
     from Clinics""")
    result = cur.fetchall()
    for row in result:
        total_sent += row[0]
        total_received += row[1]
    result = str(total_inventory) + "," + str(total_demand)
    + "," + str(total_received) + "," + str(total_sent)
    return result
