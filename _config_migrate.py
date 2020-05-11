from database.database import ApartmentsDatabase

def main():
    database = ApartmentsDatabase()
    database.migrate()

### Main ###########################
if __name__ == "__main__":
    main()