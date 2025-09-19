# Dateiname der Eingabedatei
input_file = "requirements.txt"
# Dateiname der Ausgabedatei
output_file = "requirements1.txt"

# Set, um doppelte Zeilen zu erkennen
seen_lines = set()

# Liste für eindeutige Zeilen in Originalreihenfolge
unique_lines = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        # Entferne Zeilenumbruch nur am Ende
        stripped_line = line.rstrip("\n")
        if stripped_line not in seen_lines:
            seen_lines.add(stripped_line)
            unique_lines.append(stripped_line)

# Schreibe die eindeutigen Zeilen wieder in die Datei
with open(output_file, "w", encoding="utf-8") as f:
    for line in unique_lines:
        f.write(line + "\n")

print(f"Fertig! Ausgabe gespeichert in {output_file}")
