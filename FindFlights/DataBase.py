from datetime import datetime
import sqlite3 as sql

class DataBase():

    def __init__(self):
        self.database = "ucuslar.sqlite"

    def write(self, tableName, Data, activation):

        date = Data[0]
        departure_location = Data[1]
        arrival_location = Data[2]
        departure_times = Data[3]
        arrival_times = Data[4]
        prices = Data[5]

        print("\n--> Connecting to database : " + self.database)
        try:
            db = sql.connect(self.database)
            cursor = db.cursor()
            print("\t--> Connect successfully.")
        except:
            print("\n>>> ERROR --> Could not connect to database : " + self.database)
            return "error"

        if activation == 0:
            print("--> Creating table if not exist : " + tableName)
            try:
                createTableQuery = """CREATE TABLE IF NOT EXISTS """ + tableName + """(
                            ID VARCHAR(15) PRIMARY KEY NOT NULL,
                            Date VARCHAR(30) NOT NULL,
                            Departure_Location VARCHAR(30) NOT NULL,
                            Arrival_Location VARCHAR(30) NOT NULL,
                            Departure_Times VARCHAR(30) NOT NULL,
                            Arrival_Times VARCHAR(30) NOT NULL,
                            Prices VARCHAR(30) NOT NULL)"""
                cursor.execute(createTableQuery)
            except:
                print("\n>>> ERROR --> Create table query error.")
                return "error"

        elif activation == 1:
            cursor.execute("DROP TABLE IF EXISTS " + tableName)
            print("--> Creating table : " + tableName)
            try:
                createTableQuery = """CREATE TABLE """ + tableName + """(
                                        ID VARCHAR(15) PRIMARY KEY NOT NULL,
                                        Date VARCHAR(30) NOT NULL,
                                        Departure_Location VARCHAR(30) NOT NULL,
                                        Arrival_Location VARCHAR(30) NOT NULL,
                                        Departure_Times VARCHAR(30) NOT NULL,
                                        Arrival_Times VARCHAR(30) NOT NULL,
                                        Prices VARCHAR(30) NOT NULL)"""
                cursor.execute(createTableQuery)
            except:
                print("\n>>> ERROR --> Create table query error.")
                return "error"

        print("--> Processing ID controls..")
        cursor.execute(
            "SELECT MAX(ID) FROM " + tableName + " WHERE ID LIKE '%{}%'".format(datetime.now().strftime("%Y%m%d")))
        id = cursor.fetchone()
        if id[0] != None:
            extension = str((int(id[0]) % 10000) + 1).zfill(4)
        else:
            extension = str(1).zfill(4)


        print("--> Writing data to database : " + self.database)
        try:
            for i in range(len(prices)):
                ID = datetime.now().strftime("%Y%m%d") + extension
                insertDataQuery = "INSERT INTO " + tableName + " VALUES (?,?,?,?,?,?,?)"

                cursor.execute(insertDataQuery, (ID, date, departure_location, arrival_location,
                                                 departure_times[i], arrival_times[i], prices[i]))

                extension = str(int(extension) + 1).zfill(4)
        except:
            print("\n>>> ERROR --> Could not write data to database : " + self.database)
            return "error"


        print("--> Committing to database : " + self.database)
        try:
            db.commit()
            print("\t--> Committed successfully.")
        except:
            print("\n>>> ERROR --> Could not commit to database : " + self.database + ".")


        print("--> Closing database : " + self.database)
        try:
            db.close()
            print("\t--> Close successfully.\n")
        except:
            print("\n>>> ERROR --> Could not close to database : " + self.database + "\n")


    def display(self, tableName): #düzeltilmeli

        db = sql.connect(self.database)
        cursor = db.cursor()

        cursor.execute("Select * From " + tableName)
        data = cursor.fetchall()

        print("\n" + tableName + "\n")
        for i in data:
            for j in i:
                if "\n" in j:
                    j = j.replace("\n"," ")
                print(j, end="\t|\t")
            print()

        db.close()