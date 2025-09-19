import webuntis
from datetime import date
import os
from dotenv import load_dotenv
import json

load_dotenv("D:/i guess/cuh/Kaisa (Fun Projects)/timetable/timetable.env")

username = os.getenv("WEBUNTIS_USERNAME")
password = os.getenv("WEBUNTIS_PASSWORD")
server = os.getenv("WEBUNTIS_SERVER")
school = os.getenv("WEBUNTIS_SCHOOL")
useragent = os.getenv("WEBUNTIS_USERAGENT")
name = os.getenv("WEBUNTIS_KLASSE")

s = webuntis.Session(
    server=server,
    school=school,
    username=username,
    password=password,
    useragent=useragent,
).login()

schoolyears = s.schoolyears()
current_schoolyear = next((y for y in schoolyears if y.is_current), None)
if not current_schoolyear:
    print("Kein aktuelles Schuljahr gefunden!")
    s.logout()
    exit()

startdatum = current_schoolyear.start.date()
enddatum = current_schoolyear.end.date()

klassen = s.klassen()
gefiltert = klassen.filter(name=name)

if not gefiltert:
    print("Klasse 'FG 31' nicht gefunden!")
    s.logout()
    exit()

klasse = gefiltert[0]
timetable = s.timetable(klasse=klasse, start=startdatum, end=enddatum)

stunden_liste = []
for lesson in timetable:
    if not lesson.subjects:
        continue

    start = lesson.start.strftime('%H:%M')
    end = lesson.end.strftime('%H:%M')
    subject = lesson.subjects[0].name
    status = "❌ Fällt aus" if lesson.code == 'cancelled' else "✅ Findet statt"

    stunden_liste.append({
        "date": lesson.start.strftime('%Y-%m-%d'),
        "start": start,
        "end": end,
        "subject": subject,
        "status": status
    })

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stunden.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(stunden_liste, f, ensure_ascii=False, indent=2)

print(f"{len(stunden_liste)} Einträge wurden in {json_path} gespeichert.")

s.logout()

