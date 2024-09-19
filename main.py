import sqlite3
import os

class CraneDatabase:
    def __init__(self, model_name):
        self.model_name = model_name
        self.db_name = f"CraneData/{model_name.lower().replace(' ', '_')}_crane.db"
        os.makedirs('CraneData', exist_ok=True)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS crane_data (
            jib_length REAL PRIMARY KEY,
            in_service_moment REAL,
            in_service_vertical_force REAL,
            in_service_horizontal_force REAL,
            out_of_service_moment REAL,
            out_of_service_vertical_force REAL,
            out_of_service_horizontal_force REAL
            number_of_falls REAL,
            tip_load REAL,
            max_load_radius REAL,
            wind_area REAL,
            delta_h REAL
        )
        ''')
        self.conn.commit()

    def add_data(self, jib_length, in_service_moment, in_service_vertical_force, in_service_horizontal_force,
                 out_of_service_moment, out_of_service_vertical_force, out_of_service_horizontal_force,
                 number_of_falls, tip_load, max_load_radius, wind_area, delta_h):
        self.cursor.execute('''
        INSERT OR REPLACE INTO crane_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (jib_length, in_service_moment, in_service_vertical_force, in_service_horizontal_force,
              out_of_service_moment, out_of_service_vertical_force, out_of_service_horizontal_force,
              number_of_falls, tip_load, max_load_radius, wind_area, delta_h))
        self.conn.commit()

    def get_data(self, jib_length):
        self.cursor.execute('SELECT * FROM crane_data WHERE jib_length = ?', (jib_length,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

class MastDatabase:
    def __init__(self):
        self.db_name = "MastData/mast_data.db"
        os.makedirs('MastData', exist_ok=True)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS mast_data (
            mast_model TEXT PRIMARY KEY,
            self_weight REAL,
            mast_height REAL,
            mast_wind_area REAL
        )
        ''')
        self.conn.commit()

    def add_data(self, mast_model, self_weight, mast_height, mast_wind_area):
        self.cursor.execute('''
        INSERT OR REPLACE INTO mast_data VALUES (?, ?, ?, ?)
        ''', (mast_model, self_weight, mast_height, mast_wind_area))
        self.conn.commit()

    def get_data(self, mast_model):
        self.cursor.execute('SELECT * FROM mast_data WHERE mast_model = ?', (mast_model,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

def db_operations():
    while True:
        print("\nCrane Database Management")
        print("1. Create a new crane model database")
        print("2. Add data to an existing crane model database")
        print("3. Retrieve data from a crane model database")
        print("4. Delete a crane model database")
        print("5. Return to main menu")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            model_name = input("Enter the crane model name: ")
            CraneDatabase(model_name)
            print(f"Database for {model_name} created successfully.")
        
        elif choice == '2':
            model_name = input("Enter the crane model name: ")
            db = CraneDatabase(model_name)
            
            jib_length = float(input("Enter jib length: "))
            in_service_moment = float(input("Enter in-service moment: "))
            in_service_vertical_force = float(input("Enter in-service vertical force: "))
            in_service_horizontal_force = float(input("Enter in-service horizontal force: "))
            out_of_service_moment = float(input("Enter out-of-service moment: "))
            out_of_service_vertical_force = float(input("Enter out-of-service vertical force: "))
            out_of_service_horizontal_force = float(input("Enter out-of-service horizontal force: "))
            number_of_falls = float(input("Enter number of falls: "))
            tip_load = float(input("Enter tip load: "))
            max_load_radius = float(input("Enter max load radius: "))
            wind_area = float(input("Enter wind area: "))
            delta_h = float(input("Enter delta_h: "))
            
            db.add_data(jib_length, in_service_moment, in_service_vertical_force, in_service_horizontal_force,
                        out_of_service_moment, out_of_service_vertical_force, out_of_service_horizontal_force,
                        number_of_falls, tip_load, max_load_radius, wind_area, delta_h)
            print("Data added successfully.")
            db.close()
        
        elif choice == '3':
            model_name = input("Enter the crane model name: ")
            db = CraneDatabase(model_name)
            
            jib_length = float(input("Enter jib length to retrieve data: "))
            data = db.get_data(jib_length)
            
            if data:
                print("\nRetrieved data:")
                print(f"Jib length: {data[0]}")
                print(f"In-service moment: {data[1]}")
                print(f"In-service vertical force: {data[2]}")
                print(f"In-service horizontal force: {data[3]}")
                print(f"Out-of-service moment: {data[4]}")
                print(f"Out-of-service vertical force: {data[5]}")
                print(f"Out-of-service horizontal force: {data[6]}")
                print(f"Number of falls: {data[7]}")
                print(f"Tip load: {data[8]}")
                print(f"Max load radius: {data[9]}")
                print(f"Wind area: {data[10]}")
                print(f"Delta_h: {data[11]}")
            else:
                print("No data found for the given jib length.")
            
            db.close()
        
        elif choice == '4':
            model_name = input("Enter the crane model name to delete: ")
            db_name = f"CraneData/{model_name.lower().replace(' ', '_')}_crane.db"
            if os.path.exists(db_name):
                os.remove(db_name)
                print(f"Database for {model_name} deleted successfully.")
            else:
                print(f"Database for {model_name} not found.")
        
        elif choice == '5':
            print("Returning to main menu.")
            break
        
        else:
            print("Invalid choice. Please try again.")

def mast_db_operations():
    
    while True:
        print("\nMast Database Management")
        print("1. Add or update mast data")
        print("2. Retrieve mast data")
        print("3. Return to main menu")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            db = MastDatabase()
            mast_model = input("Enter mast model: ")
            self_weight = float(input("Enter self weight: "))
            mast_height = float(input("Enter mast height: "))
            mast_wind_area = float(input("Enter mast wind area: "))
            
            db.add_data(mast_model, self_weight, mast_height, mast_wind_area)
            print("Mast data added/updated successfully.")
        
        elif choice == '2':
            mast_model = input("Enter mast model to retrieve data: ")
            data = db.get_data(mast_model)
            
            if data:
                print("\nRetrieved data:")
                print(f"Mast model: {data[0]}")
                print(f"Self weight: {data[1]}")
                print(f"Mast height: {data[2]}")
                print(f"Mast wind area: {data[3]}")
            else:
                print("No data found for the given mast model.")
            db.close()
        
        elif choice == '3':
            print("Returning to main menu.")
            break
        
        else:
            print("Invalid choice. Please try again.")
    
    db.close()

def main():
    while True:
        print("\nMain Menu")
        print("1. Edit or Add crane data")
        print("2. Edit or Add masts data")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            db_operations()
        elif choice == '2':
            mast_db_operations()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
