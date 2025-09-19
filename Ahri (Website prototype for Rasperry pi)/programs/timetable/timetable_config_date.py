# klassenaufliste:
# import webuntis

# s = webuntis.Session(
#     server='https://melete.webuntis.com',     # Deine WebUntis-URL
#     school='RBB Schwerin-Technik',           # Schulname (wie bei der Anmeldung)
#     username='fg31',
#     password='Schwerin02*',
#     useragent='Python-Test'
# ).login()

# # Alle Klassen ausgeben
# klassen = s.klassen()
# for klasse in klassen:
#     print(f"ID: {klasse.id} | Name: '{klasse.name}'")

# s.logout()



import webuntis
from datetime import date, datetime
import os
import sys
from dotenv import load_dotenv
import json

load_dotenv("D:/i guess/cuh/Kaisa (Fun Projects)/timetable/timetable.env")

username = os.getenv("WEBUNTIS_USERNAME")
password = os.getenv("WEBUNTIS_PASSWORD")
server = os.getenv("WEBUNTIS_SERVER")
school = os.getenv("WEBUNTIS_SCHOOL")
name = os.getenv("WEBUNTIS_KLASSE")  # Standardmäßig FG 31, kann aber in .env geändert werden

# Datum von Kommandozeile holen, sonst heute nehmen
if len(sys.argv) > 2:
    try:
        start = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        end = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
    except ValueError:
        print("Bitte Start- und Enddatum im Format YYYY-MM-DD übergeben!")
        sys.exit(1)
elif len(sys.argv) > 1:
    try:
        start = end = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    except ValueError:
        print("Bitte Datum im Format YYYY-MM-DD übergeben!")
        sys.exit(1)
else:
    start = end = date.today()

s = webuntis.Session(
    server='https://melete.webuntis.com',
    school='RBB Schwerin-Technik',
    username='fg31',
    password='Schwerin02*',
    useragent='Python-Test'
).login()
klassen = s.klassen()
gefiltert = klassen.filter(name=name)

if not gefiltert:
    print("Klasse 'FG 31' nicht gefunden!")
    s.logout()
    exit()

klasse = gefiltert[0]
timetable = s.timetable(klasse=klasse, start=start, end=end)

stunden = []
for lesson in timetable:
    if not lesson.subjects:
        continue

    datum = lesson.start.strftime('%Y-%m-%d')
    start_uhr = lesson.start.strftime('%H:%M')
    end_uhr = lesson.end.strftime('%H:%M')
    subject = lesson.subjects[0].name
    status = "❌ Fällt aus" if lesson.code == 'cancelled' else "✅ Findet statt"

    stunden.append((lesson.start, datum, start_uhr, end_uhr, subject, status))

stunden.sort(key=lambda x: x[0])

# Schreibe die Daten als JSON-Datei
stunden_dicts = [
    {
        "datum": datum,
        "start": start_uhr,
        "end": end_uhr,
        "subject": subject,
        "status": status
    }
    for _, datum, start_uhr, end_uhr, subject, status in stunden
]
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "stunden.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(stunden_dicts, f, ensure_ascii=False, indent=2)

s.logout()

