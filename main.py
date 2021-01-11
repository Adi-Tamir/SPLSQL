import sqlite3

from createDB import create_db, insert_info
from outputGeneration import get_order_results
from receiveShipment import receive_shipment
from sendShipment import send_shipment


def main():
    conn = sqlite3.connect('database.db')
    create_db(conn)
    insert_info(conn, 'config.txt')
    complete_orders(conn, 'orders.txt')
    pass


def complete_orders(conn, orders_path, output_path):
    with open(orders_path) as f:
        lines = f.readlines()
    for line in lines:
        arguments = line.split(',')
        if len(arguments) == 3:
            name = arguments[0]
            amount = arguments[1]
            date = arguments[2]
            receive_shipment(conn, name, amount, date)
        else:
            location = arguments[0]
            amount = arguments[1]
            send_shipment(conn, location, amount)
        order = get_order_results(conn)
        f = open(output_path, "a")
        f.write(order + '\n')
        f.close()
    pass
