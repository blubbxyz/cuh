from flask import Flask, render_template, request
import importlib

app = Flask(__name__)

# Übersicht der Programme
PROGRAMS = {
    "say_hello": {
        "title": "Say Hello",
        "description": "Greets you by name."
    },
    "calculate": {
        "title": "Calculate Sum",
        "description": "Adds two numbers."
    },
    "get_years_classes": {
        "title": "Get Years Classes",
        "description": "Zeigt die Jahrgänge und Klassen an."
    },
    "timetable_current_year": {
        "title": "Timetable Current Year",
        "description": "Zeigt den Stundenplan des aktuellen Jahres."
    },
    "timetable_stats": {
        "title": "Timetable Stats",
        "description": "Zeigt Statistiken zum Stundenplan."
    },
    "timetable_config_date": {
        "title": "Timetable Config Date",
        "description": "Konfiguriere das Stundenplandatum."
    },
    "Startmenue": {
        "title": "Startmenü",
        "description": "Startet das Hauptmenü."
    }
}

@app.route("/")
def index():
    return render_template("index.html", programs=PROGRAMS)

@app.route("/program/<prog_name>", methods=["GET", "POST"])
def run_program(prog_name):
    if prog_name not in PROGRAMS:
        return "Program not found.", 404

    result = None
    if request.method == "POST":
        # Dynamisch das Modul laden, auch aus Unterordner timetable
        if prog_name.startswith("timetable_"):
            module = importlib.import_module(f"programs.timetable.{prog_name}")
        elif prog_name == "Startmenue":
            module = importlib.import_module(f"programs.Startmenue")
        else:
            module = importlib.import_module(f"programs.{prog_name}")

        # Argumente je nach Programm
        if prog_name == "say_hello":
            name = request.form.get("name", "")
            result = module.run(name)
        elif prog_name == "calculate":
            a = request.form.get("a", "0")
            b = request.form.get("b", "0")
            result = module.run(a, b)
        else:
            result = module.run()

    return render_template("program.html", prog=PROGRAMS[prog_name], prog_name=prog_name, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
