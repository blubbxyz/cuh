def save_data(name, **kwargs):
    block = [
        f"=== speicherstand: {name} ===\n",
        "spielerinformationen:\n",
        "========================\n"
    ]
    for key, value in kwargs.items():
        block.append(f"{key}: {value}\n")
    block.append("\n")
    with open('spielereien/game.txt', 'a') as myfile:
        myfile.writelines(block)

def load_data(name):
    try:
        with open('spielereien/game.txt', 'r') as myfile:
            lines = myfile.readlines()
            found = False
            for line in lines:
                if line.strip().lower() == f"=== speicherstand: {name.lower()} ===":
                    found = True
                elif found and line.startswith("==="):
                    break
                elif found:
                    print(line.strip())
            if not found:
                print("kein speicherstand für diesen namen gefunden.")
    except FileNotFoundError:
        print("keine gespeicherten daten gefunden.")

a = input('name? ')
data = {}
while True:
    key = input('variable name (oder leer für ende): ')
    if not key:
        break
    value = input(f'{key}? ')
    data[key] = value

save_data(a, **data)
load_data(a)


# es so umschreiben das man jeglich eingabe einfach wegspeichert mit einer random variable