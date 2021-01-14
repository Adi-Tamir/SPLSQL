from PersistenceLayer.Repository import Repository
import sys


def main():
    if len(sys.argv) == 4:
        repo = Repository()
        repo.create_database()
        print("created DB")
        insert_info(sys.argv[1])
        complete_orders(sys.argv[2], sys.argv[3])
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


def complete_orders(orders_path, output_path):
    repo = Repository()
    with open(orders_path) as f:
        lines = f.readlines()
    for line in lines:
        par = line.split(',')
        if len(par) == 3:
            repo.receive_shipment(par[0], par[1], par[2])
        else:
            repo.send_shipment(par[0], par[1])
        order = repo.get_order_results()
        f = open(output_path, "a")
        f.write(order + '\n')
        f.close()
    repo.commit()
    pass


if __name__ == "__main__":
    main()

