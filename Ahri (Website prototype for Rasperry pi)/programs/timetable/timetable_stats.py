import subprocess
import json
import os
from datetime import datetime

def get_school_year(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    year = date.year
    if date.month < 8:
        return year - 1
    return year

print("Was möchtest du auswerten?")
print("1) Einen bestimmten Zeitraum")
print("2) Das gesamte aktuelle Schuljahr")
wahl = input("Bitte 1 oder 2 eingeben: ").strip()

script_dir = os.path.dirname(os.path.abspath(__file__))

if wahl == "1":
    while True:
        startdatum = input("Startdatum (YYYY-MM-DD): ")
        enddatum = input("Enddatum (YYYY-MM-DD): ")
        try:
            start_jahr = get_school_year(startdatum)
            end_jahr = get_school_year(enddatum)
        except Exception:
            print("Ungültiges Datum. Bitte erneut eingeben.")
            continue
        if start_jahr != end_jahr:
            print("Start- und Enddatum müssen im selben Schuljahr liegen!")
            continue
        break

    try:
        result = subprocess.run(
            ["python", "Kaisa (Fun Projects)/timetable/timetable_config_date.py", startdatum, enddatum],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Fehler beim Aufruf von timetable_config_date.py:")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"Fehler beim Ausführen des Zeitraums {startdatum} bis {enddatum}: {e}")

    json_path = os.path.join(script_dir, "stunden.json")

elif wahl == "2":
    try:
        result = subprocess.run(
            ["python", "Kaisa (Fun Projects)/timetable/time_table_api.py"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Fehler beim Aufruf von time_table_api.py:")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"Fehler beim Ausführen von time_table_api.py: {e}")

    json_path = os.path.join(script_dir, "stunden.json")
else:
    print("Ungültige Auswahl.")
    exit(1)

if not os.path.exists(json_path):
    print("Die Datei stunden.json wurde nicht gefunden. Es gab vermutlich einen Fehler beim Datenabruf.")
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    stunden = json.load(f)

stats = {}
for eintrag in stunden:
    fach = eintrag["subject"]
    if fach not in stats:
        stats[fach] = {"ausgefallen": 0, "gesamt": 0}
    stats[fach]["gesamt"] += 1
    if eintrag["status"].startswith("❌"):
        stats[fach]["ausgefallen"] += 1

print("\nStatistik (Fach | Ausgefallen / Gesamt | Prozent ausgefallen):")
print("-" * 55)
for fach, werte in sorted(stats.items()):
    gesamt = werte["gesamt"]
    ausgefallen = werte["ausgefallen"]
    prozent = (ausgefallen / gesamt * 100) if gesamt else 0
    print(f"{fach:20} | {ausgefallen:3} / {gesamt:3} | {prozent:5.1f}%")