import csv
import os

# Lista för att lagra persondata
people = []

# Läs CSV-filen och fyll listan med data
csv_file = 'data.csv'

# Öppna CSV-filen och läs in data om filen finns
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)  # Hoppa över header-raden

    for row in reader:
        # Kontrollera att raden har tillräcklig data
        if len(row) < 4:
            continue  # Ignorera rader med otillräcklig data

        try:
            # Konvertera och lägg till persondata till listan
            person = {
                'id': int(row[0]),
                'name': row[1],
                'year': int(row[2]),
                'tracks': int(row[3])
            }
            people.append(person)
        except ValueError:
            # Hantera ogiltiga rader (t.ex. om värden inte kan konverteras)
            print(f"Ogiltig data på rad: {row}")


# Funktion för att visa alla poster i tabellform
def display_table():
    print("\n\n# | NAMN                     | ÅR   | TOTALA SPÅR")
    print("--|--------------------------|-------|-------------")
    for person in people:
        # Formatera och visa varje person i tabellen
        print(f"{person['id']:<2} | {person['name']:<24.24} | {person['year']:<5} | {person['tracks']:<11}")


# Funktion för att lägga till en ny post
def add_entry():
    name = input("Ange namn: ")
    year = valid_year("Ange år (YYYY): ")
    tracks = valid_track("Ange antal spår (1-25): ")
    new_id = max([person['id'] for person in people], default=0) + 1  # Generera nytt ID
    people.append({'id': new_id, 'name': name, 'year': year, 'tracks': tracks})
    print("Posten har lagts till.")


# Funktion för att ta bort en post baserat på ID
def remove_entry():
    entry_id = valid_int("Ange ID för posten som ska tas bort: ")
    global people
    # Filtrera bort posten med matchande ID
    people = [person for person in people if person['id'] != entry_id]
    print("Posten har tagits bort.")


# Funktion för att uppdatera en post
def update_entry():
    entry_id = valid_int("Ange ID för posten som ska uppdateras: ")
    for person in people:
        if person['id'] == entry_id:
            column = input("Ange vilken kolumn som ska uppdateras (name, year, tracks): ")
            if column not in ['name', 'year', 'tracks']:
                print("Ogiltig kolumn.")
                return
            # Validera och uppdatera rätt kolumn
            if column == 'year':
                person[column] = valid_year(f"Ange det nya värdet för {column} (YYYY): ")
            elif column == 'tracks':
                person[column] = valid_track(f"Ange det nya värdet för {column} (1-25): ")
            elif column == 'name':
                person[column] = input(f"Ange det nya värdet för {column}: ")
            print("Posten har uppdaterats.")
            return
    print("Ingen post hittades med det angivna ID:t.")


# Funktion för att spara ändringar till CSV-filen
def save_to_csv():
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'year', 'tracks'])  # Skriv header
        for person in people:
            writer.writerow([person['id'], person['name'], person['year'], person['tracks']])
    print("Ändringar har sparats till CSV-filen.")


# Funktion för att validera ett år inom intervallet 2000–2050
def valid_year(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            year = int(user_input)
            if 2000 <= year <= 2050:
                return year
            else:
                print("Ogiltigt år. Ange ett år mellan 2000 och 2050.")
        else:
            print("Ogiltigt värde. Ange ett år i formatet YYYY (t.ex. 2024).")


# Funktion för att validera antal spår inom intervallet 1–25
def valid_track(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            track = int(user_input)
            if 1 <= track <= 25:
                return track
            else:
                print("Ogiltigt värde. Ange 1-25.")
        else:
            print("Ogiltigt värde. Ange 1-25.")


# Funktion för att validera ett heltal
def valid_int(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)


# Rensa konsolen
os.system('cls')

# Användarmenyn
while True:
    print("\n\n1. Visa tabell")
    print("2. Lägg till en post")
    print("3. Ta bort en post")
    print("4. Ändra en post")
    print("5. Spara ändringar till fil")
    print("6. Avsluta/Spara")

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
        save_to_csv()
    elif choice == "6":  # Sparar och avslutar
        save_to_csv()
        break
    else:
        print("Ogiltigt val, försök igen.")
