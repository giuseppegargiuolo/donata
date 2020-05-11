from database.database import ApartmentsDatabase

def main():
    database = ApartmentsDatabase()
    database.session.execute('DROP DATABASE apartments_dev;')
    database.session.execute('CREATE DATABASE apartments_dev CHARACTER SET utf8 COLLATE utf8_bin;')

### Main ###########################
if __name__ == "__main__":
    main()