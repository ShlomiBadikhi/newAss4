import sqlite3
import atexit
import sys
import persistence


def main():
    config = sys.argv[1]
    orders = sys.argv[2]
    output = sys.argv[3]
    database = sys.argv[4]

    repo = persistence._Repository(database)
    atexit.register(repo._close)
    repo.create_tables()





if __name__ == '__main__':
    main()
