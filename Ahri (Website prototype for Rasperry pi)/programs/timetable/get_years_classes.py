import webuntis
from datetime import datetime
from dotenv import load_dotenv
import os
import sys

load_dotenv("D:/i guess/cuh/Kaisa (Fun Projects)/timetable/timetable.env")

username = os.getenv("WEBUNTIS_USERNAME")
password = os.getenv("WEBUNTIS_PASSWORD")
server = os.getenv("WEBUNTIS_SERVER")
school = os.getenv("WEBUNTIS_SCHOOL")
useragent = os.getenv("WEBUNTIS_USERAGENT")

if not all([username, password, server, school, useragent]):
    print("Fehler: Mindestens eine WebUntis-Umgebungsvariable ist nicht gesetzt!")
    exit(1)

session = webuntis.Session(
    server=server,
    school=school,
    username=username,
    password=password,
    useragent=useragent,
).login()

years = session.schoolyears()
print("Verfügbare Schuljahre:")
for y in years:
    print(f"- ID {y.id}: {y.name} ({y.start.strftime('%Y-%m-%d')} bis {y.end.strftime('%Y-%m-%d')})")

if len(sys.argv) > 1:
    try:
        chosen_id = int(sys.argv[1])
    except ValueError:
        print("Ungültige Schuljahr-ID übergeben.")
        session.logout()
        exit(1)
    chosen_year = next((y for y in years if y.id == chosen_id), None)
    if not chosen_year:
        print("Ungültige Schuljahr-ID.")
        session.logout()
        exit(1)
else:
    chosen_id = None
    while chosen_id is None:
        eingabe = input("Bitte Schuljahr-ID eingeben: ").strip()
        if not eingabe.isdigit():
            print("Bitte eine gültige Zahl eingeben.")
            continue
        chosen_id = int(eingabe)
        chosen_year = next((y for y in years if y.id == chosen_id), None)
        if not chosen_year:
            print("Ungültige Schuljahr-ID.")
            chosen_id = None

print(f"\nGewähltes Schuljahr: {chosen_year.name} ({chosen_year.start.strftime('%Y-%m-%d')} bis {chosen_year.end.strftime('%Y-%m-%d')})")

klassen = session.klassen(schoolyear=chosen_year)
print(f"\nKlassen im Schuljahr {chosen_year.name}:")
for k in klassen:
    print(f"- ID {k.id}: {k.name}")

session.logout()
