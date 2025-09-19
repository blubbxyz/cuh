# file: pwd_hash_demo.py
"""
Kleines Demo-Tool:
- Speichert Accounts im Format username|riot#tag:HASH (anstatt Klartextpasswort)
- Migration: falls accounts_plain.env existiert, wird sie gehashed in accounts_hashed.env
- Einfaches CLI: add, verify, list, migrate
"""

from argon2 import PasswordHasher, exceptions
import os

PLAIN_FILE = "accounts_plain.env"   # optional: alte Datei mit Klartextpasswörtern
HASHED_FILE = "accounts_hashed.env" # neue Datei mit Argon2-Hashes

ph = PasswordHasher()  # Standard-Parameter (sicher)

def parse_line(line):
    # erwartet z. B.: username|summoner#tag:password
    line = line.strip()
    if not line:
        return None
    if ":" in line:
        user_summoner, pwd = line.split(":", 1)
    else:
        user_summoner, pwd = line, ""
    if "|" in user_summoner:
        username, name_tag = user_summoner.split("|", 1)
    else:
        username, name_tag = "", user_summoner
    if "#" in name_tag:
        name, tag = name_tag.split("#", 1)
    else:
        name, tag = name_tag, ""
    return {"username": username, "name": name, "tag": tag, "password": pwd}

def load_hashed_accounts():
    accounts = []
    if not os.path.exists(HASHED_FILE):
        return accounts
    with open(HASHED_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line)
            if parsed:
                accounts.append(parsed)
    return accounts

def save_hashed_accounts(accounts):
    with open(HASHED_FILE, "w", encoding="utf-8") as f:
        for acc in accounts:
            # speichern: username|name#tag:HASH
            user_summoner = f"{acc['username']}|{acc['name']}#{acc['tag']}" if acc['tag'] else f"{acc['username']}|{acc['name']}"
            f.write(f"{user_summoner}:{acc['password']}\n")

def migrate_plain_to_hashed():
    if not os.path.exists(PLAIN_FILE):
        print(f"Keine {PLAIN_FILE} zum migrieren gefunden.")
        return
    accounts = []
    with open(PLAIN_FILE, "r", encoding="utf-8") as f:
        for line in f:
            p = parse_line(line)
            if not p:
                continue
            pwd = p["password"]
            if pwd:
                hashed = ph.hash(pwd)
                p["password"] = hashed
                accounts.append(p)
    save_hashed_accounts(accounts)
    print(f"Migriert {len(accounts)} Accounts nach {HASHED_FILE}.")
    # Hinweis: Falls du die Klartextdatei nicht mehr brauchst, lösche sie manuell.

def add_account():
    riot_name = input("Riot-Name (z.B. blubb#1234): ").strip()
    username = input("Dein Username (z.B. cookieblubb): ").strip()
    password = input("Passwort: ").strip()
    if "#" in riot_name:
        name, tag = riot_name.split("#", 1)
    else:
        name, tag = riot_name, ""
    hashed = ph.hash(password)
    accounts = load_hashed_accounts()
    accounts.append({"username": username, "name": name, "tag": tag, "password": hashed})
    save_hashed_accounts(accounts)
    print("Account hinzugefügt (Passwort als Hash gespeichert).")

def verify_account():
    riot_name = input("Riot-Name zum Prüfen (z.B. blubb#1234): ").strip()
    if "#" in riot_name:
        name, tag = riot_name.split("#", 1)
    else:
        name, tag = riot_name, ""
    pwd_try = input("Passwort Eingabe: ").strip()
    accounts = load_hashed_accounts()
    found = False
    for acc in accounts:
        if acc["name"] == name and acc["tag"] == tag:
            found = True
            try:
                if ph.verify(acc["password"], pwd_try):
                    print("Passwort korrekt!")
                    # Optional: rehashing (falls Parameter geändert wurden)
                    if ph.check_needs_rehash(acc["password"]):
                        print("Rehash nötig — aktualisiere Hash.")
                        acc["password"] = ph.hash(pwd_try)
                        save_hashed_accounts(accounts)
                else:
                    print("Passwort falsch.")
            except exceptions.VerifyMismatchError:
                print("Passwort falsch.")
            except Exception as e:
                print("Fehler beim Verifizieren:", e)
    if not found:
        print("Account nicht gefunden.")

def list_accounts():
    accounts = load_hashed_accounts()
    if not accounts:
        print("Keine Accounts gefunden.")
        return
    for i, acc in enumerate(accounts, 1):
        tag = f"#{acc['tag']}" if acc['tag'] else ""
        print(f"{i}. {acc['name']}{tag} | {acc['username']} | HASH: {acc['password'][:16]}...")

def main():
    while True:
        print("\n--- Argon2 Hash Demo ---")
        print("1) Migrate plaintext -> hashed (accounts_plain.env -> accounts_hashed.env)")
        print("2) Add account (neuen Account mit Hash speichern)")
        print("3) Verify account (Passwort prüfen)")
        print("4) List accounts (zeigt gekürzte Hashes)")
        print("5) Exit")
        choice = input("Wahl: ").strip()
        if choice == "1":
            migrate_plain_to_hashed()
        elif choice == "2":
            add_account()
        elif choice == "3":
            verify_account()
        elif choice == "4":
            list_accounts()
        elif choice == "5":
            break
        else:
            print("Ungültig.")

if __name__ == "__main__":
    main()
