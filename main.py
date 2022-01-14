import sqlite3
import atexit
import sys
import persistence
import os

def orderAndUpdate(repo, location, topping):
    repo.


def main():
    # read terminal arguments
    config = open(sys.argv[1], "r")
    orders = open(sys.argv[2], "r")
    output = open(sys.argv[3], "w")
    database = sys.argv[4]

    # figure out num of hats and num of suppliers
    first_line_config = config.readline()
    first_line_split = first_line_config.split(",")
    num_of_hats = int(first_line_split[0])
    num_of_suppliers = int(first_line_split[1][0:len(first_line_split[1])-1])

    # create repository
    repo = persistence._Repository(database)
    atexit.register(repo._close)
    repo.create_tables()

    # iterate over all hats
    for i in range(0,num_of_hats):
        # get hat variables
        next_line = config.readline()
        hat_variables = next_line.split(',')
        hat_variables[3] = hat_variables[3][0:len(hat_variables[3])-1]

        # create and insert next hat
        next_hat = persistence.Hat(int(hat_variables[0]), hat_variables[1], int(hat_variables[2]), int(hat_variables[3]))
        repo.hats.insert(next_hat)

    # iterate over all suppliers
    for i in range(0, num_of_suppliers):
        # get supplier variables
        next_line = config.readline()
        supplier_variables = next_line.split(',')
        supplier_variables[1] = supplier_variables[1][0:len(supplier_variables[1]) - 1]

        # create and insert next supplier
        next_supplier = persistence.Supplier(int(supplier_variables[0]), supplier_variables[1],)
        repo.suppliers.insert(next_supplier)

    for order in orders:
        # read next order
        order = order.strip()
        order_split = order.split(',')
        location = order_split[0]
        topping = order_split[1]

        # order and update
        supplier = orderAndUpdate(repo, location, topping)

        # insert to output file
        if supplier != "":
            output.write(topping + "," + supplier + "," + location + "\n")

    output.close()
    orders.close()
    config.close()


if __name__ == '__main__':
    main()
