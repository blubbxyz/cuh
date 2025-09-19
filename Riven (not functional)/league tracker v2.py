import os
import keyboard
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from dotenv import load_dotenv, set_key, dotenv_values

# ---------------------------
# Setup
# ---------------------------

ENV_FILE = "lol.env"
load_dotenv(ENV_FILE)

API_KEY = os.getenv("API_KEY", "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
ACCOUNT_FILE = "accounts.env"  # Format per line: username|summoner#tag:password
REGION = "EUW1"

# RiotWatcher objects (werden neu initialisiert wenn key geändert wird)
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)

# ---------------------------
# Menu helpers
# ---------------------------
def arrow_menu_vertical(title, options):
    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(title + "\n")
        for i, opt in enumerate(options):
            if i == idx:
                print(f"> {opt.upper()} <")
            else:
                print(f"  {opt}  ")
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "down":
                idx = (idx + 1) % len(options)
            elif event.name == "up":
                idx = (idx - 1) % len(options)
            elif event.name == "enter":
                return options[idx]

def arrow_menu_horizontal(title, options):
    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(title + "\n")
        for i, opt in enumerate(options):
            if i == idx:
                print(f"[{opt.upper()}]", end="  ")
            else:
                print(f" {opt} ", end="  ")
        print("\n\nUse ← / → to move, Enter to select.")
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "right":
                idx = (idx + 1) % len(options)
            elif event.name == "left":
                idx = (idx - 1) % len(options)
            elif event.name == "enter":
                return options[idx]

# ---------------------------
# Account helpers
# ---------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_accounts():
    accounts = []
    if not os.path.isfile(ACCOUNT_FILE):
        return accounts
    with open(ACCOUNT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                user_summoner, password = line.split(":", 1)
            else:
                user_summoner, password = line, ""
            if "|" in user_summoner:
                username, name_tag = user_summoner.split("|", 1)
            else:
                username, name_tag = "", user_summoner
            if "#" in name_tag:
                name, tag = name_tag.split("#", 1)
            else:
                name, tag = name_tag, ""
            accounts.append({"username": username, "name": name, "tag": tag, "password": password})
    return accounts

def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w", encoding="utf-8") as f:
        for acc in accounts:
            line = f"{acc['username']}|{acc['name']}#{acc['tag']}:{acc['password']}" if acc["tag"] else f"{acc['username']}|{acc['name']}:{acc['password']}"
            f.write(line + "\n")

def display_ranks(accounts, api_valid):
    print("--- Current SoloQ Ranks ---")
    for acc in accounts:
        try:
            if api_valid:
                account_data = riot_watcher.account.by_riot_id("EUROPE", acc["name"], acc["tag"])
                puuid = account_data["puuid"]
                ranked_stats = lol_watcher.league.by_puuid(REGION.lower(), puuid)
                soloq = [r for r in ranked_stats if r["queueType"] == "RANKED_SOLO_5x5"]
                soloq_rank = f"{soloq[0]['tier']} {soloq[0]['rank']} ({soloq[0]['leaguePoints']} LP)" if soloq else "Unranked"
            else:
                soloq_rank = "N/A"
            print(f"{acc['name']}#{acc['tag']} | {acc['username']} | PW: {acc['password']} | SoloQ: {soloq_rank}")
        except ApiError as e:
            print(f"{acc['name']}#{acc['tag']} | {acc['username']} | PW: {acc['password']} | Error: {e.response.status_code}")

def add_account(accounts):
    riot_name = input("Enter Riot in-game name (e.g., blubb#xdd): ")
    username = input("Enter your own username (e.g., cookieblubb): ")
    password = input("Enter password: ")
    if "#" in riot_name:
        name, tag = riot_name.split("#", 1)
    else:
        name, tag = riot_name, ""
    accounts.append({"username": username, "name": name, "tag": tag, "password": password})
    save_accounts(accounts)
    print("Account added!")

def delete_account(accounts):
    print("Accounts:")
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. {acc['name']}#{acc['tag']}")
    index = int(input("Which account do you want to delete? (Number) ")) - 1
    if 0 <= index < len(accounts):
        removed = accounts.pop(index)
        save_accounts(accounts)
        print(f"{removed['name']} removed!")
    else:
        print("Invalid number.")

def change_api_key():
    global API_KEY, lol_watcher, riot_watcher
    new_key = input("Enter a valid new API-Key: ")
    API_KEY = new_key
    lol_watcher = LolWatcher(API_KEY)
    riot_watcher = RiotWatcher(API_KEY)
    set_key(ENV_FILE, "API_KEY", API_KEY)
    print("API-Key updated and saved to .env!")

# ---------------------------
# Main Menu
# ---------------------------
def main_menu():
    accounts = load_accounts()

    api_valid = True
    try:
        lol_watcher.summoner.by_puuid(REGION.lower(), "test-puuid-invalid")
    except ApiError as e:
        if e.response.status_code == 401:
            api_valid = False

    while True:
        clear()
        print("=== League of Legends Tracker ===")
        if not api_valid:
            print("⚠️ Warning: Your API-Key is invalid or expired!\n")

        display_ranks(accounts, api_valid)
        
        # Menü mit Pfeiltasten statt Input
        options = ["Add Account", "Delete Account", "Exit"]
        if not api_valid:
            options.append("Change API-Key")

        choice = arrow_menu_vertical("Choose an option:", options)

        if choice == "Add Account":
            add_account(accounts)
        elif choice == "Delete Account":
            delete_account(accounts)
        elif choice == "Exit":
            print("Bye!")
            break
        elif choice == "Change API-Key":
            change_api_key()
            api_valid = True

        input("\nPress Enter to continue...")

# ---------------------------
# Start
# ---------------------------
if __name__ == "__main__":
    main_menu()
