import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from dotenv import load_dotenv, set_key, dotenv_values


# ---------------------------
# Configuration
# ---------------------------
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

API_KEY = os.getenv("API_KEY", "RGAPI-bac687ed-ddc5-4331-abc-4ba320c9e1b5")
ACCOUNT_FILE = "accounts.txt"  # Format per line: username|summoner#tag:password
REGION = "EUW1"

# RiotWatcher objects (can be re-initialized if key changes)
lol_watcher = LolWatcher(API_KEY)
riot_watcher = RiotWatcher(API_KEY)

# ---------------------------
# Helper Functions
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
            # Format: username|summoner#tag:password
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
            print(f"{acc['name']}#{acc['tag']} | {acc['username']} | Password: {acc['password']} | SoloQ: {soloq_rank}")
        except ApiError as e:
            print(f"{acc['name']}#{acc['tag']} | {acc['username']} | Password: {acc['password']} | Error: {e.response.status_code}")

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
    # Save to .env
    set_key(ENV_FILE, "API_KEY", API_KEY)
    print("API-Key updated and saved to .env!")

# ---------------------------
# Menu
# ---------------------------
def main_menu():
    accounts = load_accounts()
    
    # Check if API-Key is valid
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
            print("⚠️ Warning: Your API-Key is invalid or expired! SoloQ ranks cannot be loaded.\n")

        display_ranks(accounts, api_valid)
        print("\nOptions:")
        print("1. Add Account")
        print("2. Delete Account")
        print("3. Exit")
        if not api_valid:
            print("4. Change API-Key")
        choice = input("Choose: ")
        if choice == "1":
            add_account(accounts)
        elif choice == "2":
            delete_account(accounts)
        elif choice == "3":
            print("Bye!")
            break
        elif choice == "4" and not api_valid:
            change_api_key()
            api_valid = True
        else:
            print("Invalid choice.")
        input("\nPress Enter to continue...")

# ---------------------------
# Start Program
# ---------------------------
if __name__ == "__main__":
    main_menu()

