import sqlite3

from createDB import create_db, insert_info
from outputGeneration import get_order_results
from receiveShipment import receive_shipment
from sendShipment import send_shipment

from Repository import Repository
import sys


def main():
    repo = Repository()
    repo.create_database()
    repo.insert_info(sys.argv[0])
    repo.complete_orders(sys.argv[1], sys.argv[2])
    pass



