from PersistenceLayer.DTOs import Vaccines
from PersistenceLayer.Repository import Repository
import sys


def main():
    if len(sys.argv) == 4:
        repo = Repository()
        repo.create_database()
        insert_info(sys.argv[1])
        complete_orders(sys.argv[2], sys.argv[3], repo)
        pass
    else:
        print("Not given 3 arguments")


def insert_info(config_path):
    repo = Repository()
    with open(config_path) as f:
        lines = f.readlines()
    nums_line = lines[0]
    nums = nums_line.replace('\n', '').split(",")

    end = len(lines) - 1
    start = end - int(nums[3]) + 1
    for line in range(start, end + 1):
        logistic = repo.create_logistics(lines[line].replace('\n', ''))
        repo.logistics.insert_l(logistic)

    end = start - 1
    start = end - int(nums[2]) + 1
    for line in range(start, end + 1):
        clinic = repo.create_clinics(lines[line].replace('\n', ''))
        repo.clinics.insert_c(clinic)

    end = start - 1
    start = end - int(nums[1]) + 1
    for line in range(start, end + 1):
        supplier = repo.create_supplier(lines[line].replace('\n', ''))
        repo.suppliers.insert(supplier)

    end = start - 1
    start = end - int(nums[0]) + 1
    for line in range(start, end + 1):
        vaccine = repo.create_vaccines(lines[line].replace('\n', ''))
        repo.vaccines.insert(vaccine)
    repo.commit()
    pass


def complete_orders(orders_path, output_path, repo):
    #repo = Repository()
    with open(orders_path) as f:
        lines = f.readlines()
    for line in lines:
        par = line.split(',')
        if len(par) == 3:
            receive_shipment(par[0], par[1], par[2], repo)
        else:
            send_shipment(par[0], par[1], repo)
        order = get_order_results(repo)
        f = open(output_path, "a")
        f.write(order + '\n')
        f.close()
    repo.commit()
    pass


def receive_shipment(name, amount, date, repo):
    #repo = Repository()
    next_id = int(repo.vaccines.get_max_id()[0]) + 1
    supplier = repo.suppliers.find_by_name(name)
    vaccine = Vaccines(next_id, date, supplier.name, amount)
    repo.vaccines.insert(vaccine)
    repo.logistics.update_received(supplier.logistic, amount)
    pass


def send_shipment(location, amount, repo):
    #repo = Repository()
    repo.clinics.update(amount, location)
    amount = int(amount)
    while int(amount) > 0:
        vaccine_entry = repo.vaccines.find_oldest_vaccine()
        if int(vaccine_entry.quantity) > int(amount):
            repo.vaccines.update_vaccine_entry(amount, vaccine_entry.id)
            logistic_id = repo.clinics.find_by_location(location).logistic
            repo.logistics.update_sent(logistic_id, amount)
            amount = 0
        else:
            amount -= vaccine_entry.quantity
            repo.vaccines.delete_entry((vaccine_entry.id,))
            logistic_id = repo.clinics.find_by_location(location).logistic
            repo.logistics.update_sent(logistic_id, vaccine_entry.quantity)
    pass


def get_order_results(repo):
    #repo = Repository()
    total_inventory = 0
    total_demand = 0
    total_received = 0
    total_sent = 0
    result = repo.vaccines.amount()
    for row in result:
        total_inventory += row[0]
    result = repo.clinics.demand()
    for row in result:
        total_demand += row[0]
    result = repo.logistics.sent_received()
    for row in result:
        total_sent += row[0]
        total_received += row[1]
    result = str(total_inventory) + "," + str(total_demand) + "," + str(total_received) + "," + str(total_sent)
    return result


if __name__ == "__main__":
    main()

