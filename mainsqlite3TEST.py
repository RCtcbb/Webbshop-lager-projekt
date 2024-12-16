import sqlite3
import csv

# Skapa en in-memory SQLite-databas
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Skapa en tabell för att lagra persondata
cursor.execute('''
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT,
    year INTEGER,
    tracks INTEGER
)
''')

# Läs CSV-filen och lägg till data i databasen
csv_file = 'data.csv'

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)  # Hoppa över header-raden

    for row in reader:
        if len(row) < 4:
            continue  # Ignorera rader med otillräcklig data

        id = row[0]
        name = row[1]
        try:
            year = int(row[2])  # Försök konvertera år till heltal
            tracks = int(row[3])  # Försök konvertera spår till heltal
        except ValueError:
            continue  # Om data inte är korrekt, hoppa över raden
        
        # Lägg till personen i databasen
        cursor.execute('INSERT INTO people (id, name, year, tracks) VALUES (?, ?, ?, ?)', (id, name, year, tracks))

# Spara ändringar i databasen
conn.commit()

# Funktion för att visa alla poster i tabellen
def display_table():
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()
    print("# | NAMN                     | ÅR   | TOTALA SPÅR")
    print("--|--------------------------|-------|-------------")
    for row in rows:
        print(f"{row[0]:<2} | {row[1]:<24} | {row[2]:<5} | {row[3]:<11}")

# Funktion för att lägga till en ny post
def add_entry():
    name = input("Ange namn: ")
    year = int(input("Ange år: "))
    tracks = int(input("Ange antal spår: "))
    cursor.execute('INSERT INTO people (name, year, tracks) VALUES (?, ?, ?)', (name, year, tracks))
    conn.commit()
    print("Posten har lagts till.")

# Funktion för att ta bort en post baserat på ID
def remove_entry():
    entry_id = int(input("Ange ID för posten som ska tas bort: "))
    cursor.execute('DELETE FROM people WHERE id = ?', (entry_id,))
    conn.commit()
    print("Posten har tagits bort.")

# Funktion för att uppdatera en post
def update_entry():
    entry_id = int(input("Ange ID för posten som ska uppdateras: "))
    column = input("Ange vilken kolumn som ska uppdateras (name, year, tracks): ")
    new_value = input("Ange det nya värdet: ")

    # Om kolumnen är "year" eller "tracks", konvertera det nya värdet till heltal
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

    # Hantera användarens val
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

# Stäng databasen efter att alla operationer är slutförda
conn.close()
