import sqlite3
import csv

# Skapa en in-memory SQLite-databas
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Skapa en tabell i SQLite-databasen
cursor.execute('''
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT,
    year INTEGER,
    tracks INTEGER
)
''')

# Läs in CSV-filen
csv_file = 'data.csv'  # Set the path to your CSV file

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    
    # Skipping header row if it exists
    next(reader, None)  # Skips the header row

    for row in reader:
        print(f"Processing row: {row}")  # Debugging: print the row to inspect it
        
        # Ignore rows that are empty or don't have enough columns
        if len(row) < 4:  # Check if there are enough columns (id, name, year, tracks)
            print(f"Raden ignoreras på grund av otillräcklig data: {row}")
            continue

        # Extract data for each column
        id = row[0]
        name = row[1]
        try:
            year = int(row[2])  # Convert year to integer
            tracks = int(row[3])  # Convert tracks to integer
        except ValueError:
            print(f"Ogiltig data för år eller antal spår för {name}, raden ignoreras.")
            continue
        
        # Insert the row into the database
        cursor.execute('INSERT INTO people (id, name, year, tracks) VALUES (?, ?, ?, ?)', (id, name, year, tracks))

# Spara ändringar och stäng anslutningen
conn.commit()

def display_table():
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()

    print("# | NAMN                     | ÅR   | TOTALA SPÅR")
    print("--|--------------------------|-------|-------------")
    for row in rows:
        print(f"{row[0]:<2} | {row[1]:<24} | {row[2]:<5} | {row[3]:<11}")

def add_entry():
    name = input("Ange namn: ")
    year = int(input("Ange år: "))
    tracks = int(input("Ange antal spår: "))
    cursor.execute('INSERT INTO people (name, year, tracks) VALUES (?, ?, ?)', (name, year, tracks))
    conn.commit()
    print("Posten har lagts till.")

def remove_entry():
    entry_id = int(input("Ange ID för posten som ska tas bort: "))
    cursor.execute('DELETE FROM people WHERE id = ?', (entry_id,))
    conn.commit()
    print("Posten har tagits bort.")

def update_entry():
    entry_id = int(input("Ange ID för posten som ska uppdateras: "))
    column = input("Ange vilken kolumn som ska uppdateras (name, year, tracks): ")
    new_value = input("Ange det nya värdet: ")

    if column == "year" or column == "tracks":
        new_value = int(new_value)

    cursor.execute(f'UPDATE people SET {column} = ? WHERE id = ?', (new_value, entry_id))
    conn.commit()
    print("Posten har uppdaterats.")

# Användarmenyn
while True:
    print("\n1. Visa tabell")
    print("2. Lägg till en post")
    print("3. Ta bort en post")
    print("4. Ändra en post")
    print("5. Avsluta")

    choice = input("Välj ett alternativ: ")

    if choice == "1":
        display_table()
    elif choice == "2":
        add_entry()
    elif choice == "3":
        remove_entry()
    elif choice == "4":
        update_entry()
    elif choice == "5":
        break
    else:
        print("Ogiltigt val, försök igen.")

# Stäng databasen
conn.close()
