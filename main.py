from PersistenceLayer.Repository import Repository
import sys


def main():
    if len(sys.argv) == 4:
        repo = Repository()
        repo.create_database()
        print("created DB")
        repo.insert_info(sys.argv[1])
        repo.complete_orders(sys.argv[1], sys.argv[2])
        pass
    else:
        print("Not given 3 arguments")


if __name__ == "__main__":
    main()

