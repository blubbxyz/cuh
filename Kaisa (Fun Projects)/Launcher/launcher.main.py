import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, Label, StringVar
import subprocess
import shutil
from PIL import Image, ImageTk
import win32gui
import win32ui
import win32con
import tkinter.messagebox as msgbox

# ---------------------------
# FIX FOR PYINSTALLER EXE
# ---------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Correct folder paths
BASE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
GAMES_PATH = os.path.join(BASE_PATH, "Games")
print("REAL BASE_PATH =", BASE_PATH)
print("REAL GAMES_PATH =", GAMES_PATH)

# ---------------- Game config ----------------
def get_game_config(game):
    config_file = os.path.join(GAMES_PATH, game, "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return {}

def save_game_config(game, config):
    config_file = os.path.join(GAMES_PATH, game, "config.json")
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def choose_exe(game):
    path = filedialog.askopenfilename(title=f"Choose EXE for {game}", filetypes=[("Programs", "*.exe *.bat")])
    if path:
        config = get_game_config(game)
        config["exe"] = path
        save_game_config(game, config)
        return path
    return None

def choose_save_path(game):
    path = simpledialog.askstring("Savegame Folder", f"Please enter the AppData save folder for {game}:\n(e.g. LocalLow\\<game folder>)")
    if path:
        config = get_game_config(game)
        config["save_path"] = path
        save_game_config(game, config)
        return path
    return None

# ---------------- Copying saves ----------------
def copy_with_progress(src, dst):
    files = [os.path.join(r, f) for r, _, fs in os.walk(src) for f in fs]
    total = len(files)
    if total == 0:
        return

    progress_win = Toplevel()
    progress_win.title("Copying saves...")
    progress_label_var = StringVar()
    progress_label_var.set(f"Copying 0 / {total} files")
    Label(progress_win, textvariable=progress_label_var).pack(padx=20, pady=20)
    progress_win.update()

    for i, file in enumerate(files, start=1):
        rel_path = os.path.relpath(file, src)
        dst_file = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        shutil.copy2(file, dst_file)
        progress_label_var.set(f"Copying {i} / {total} files")
        progress_win.update()

    progress_win.destroy()

def sync_saves_to_pc(game):
    config = get_game_config(game)
    save_path = config.get("save_path")
    if not save_path:
        return
    appdata_root = os.path.join(os.path.expanduser("~"), "AppData")
    local = os.path.join(appdata_root, save_path)
    usb = os.path.join(GAMES_PATH, game, "Saves")
    if os.path.exists(usb):
        os.makedirs(local, exist_ok=True)
        copy_with_progress(usb, local)

def sync_saves_to_usb(game):
    config = get_game_config(game)
    save_path = config.get("save_path")
    if not save_path:
        return
    appdata_root = os.path.join(os.path.expanduser("~"), "AppData")
    local = os.path.join(appdata_root, save_path)
    usb = os.path.join(GAMES_PATH, game, "Saves")
    if os.path.exists(local):
        os.makedirs(usb, exist_ok=True)
        copy_with_progress(local, usb)

# ---------------- Extract EXE icon ----------------
def get_icon_from_exe(exe_path, size=(32, 32)):
    large, _ = win32gui.ExtractIconEx(exe_path, 0)
    if not large:
        return None
    hicon = large[0]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, size[0], size[1])
    hdc_mem = hdc.CreateCompatibleDC()
    hdc_mem.SelectObject(hbmp)
    win32gui.DrawIconEx(hdc_mem.GetSafeHdc(), 0, 0, hicon, size[0], size[1], 0, 0, win32con.DI_NORMAL)
    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)
    image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    win32gui.DestroyIcon(hicon)
    hdc_mem.DeleteDC()
    hdc.DeleteDC()
    return image

# ---------------- Start game ----------------
def start_game(game):
    config = get_game_config(game)
    exe = config.get("exe")
    if not exe or not os.path.exists(exe):
        exe = choose_exe(game)
        if not exe:
            return
    save_path = config.get("save_path")
    if not save_path:
        save_path = choose_save_path(game)
        if not save_path:
            return
    sync_saves_to_pc(game)
    try:
        proc = subprocess.Popen(exe)
        proc.wait()
        sync_saves_to_usb(game)
    except Exception as e:
        print(f"Error starting game: {e}")

# ---------------- UI SETUP ------------------
root = tk.Tk()
root.title("Launcher")
root.geometry("215x400")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ---------------- read games robust ----------------
print("GAMES_PATH =", GAMES_PATH)
if not os.path.exists(GAMES_PATH):
    try:
        os.makedirs(GAMES_PATH, exist_ok=True)
    except Exception as e:
        msgbox.showerror("Error", f"Could not create Games folder:\n{GAMES_PATH}\n\n{e}")
        raise
    msgbox.showinfo(
        "Games folder created",
        f"No 'Games' folder was found.\nA new folder was created at:\n{GAMES_PATH}\n\n"
        "Put each game into its own subfolder inside that folder and restart the launcher."
    )
    games = []
else:
    games = []
    try:
        for folder in os.listdir(GAMES_PATH):
            folder_path = os.path.join(GAMES_PATH, folder)
            if os.path.isdir(folder_path):
                games.append(folder)
    except Exception as e:
        msgbox.showerror("Error reading Games folder", str(e))
        games = []

if not games:
    msgbox.showinfo(
        "No games found",
        f"No game folders found in:\n{GAMES_PATH}\n\n"
        "Create one folder per game (Example: Games\\Kaisa) and restart the launcher."
    )

# ---------------- make buttons ----------------
button_images = {}
for game in games:
    config = get_game_config(game)
    exe = config.get("exe")
    photo = None
    if exe and os.path.exists(exe):
        img = get_icon_from_exe(exe)
        if img:
            photo = ImageTk.PhotoImage(img)
            button_images[game] = photo
    btn = tk.Button(
        scrollable_frame,
        text=game,
        image=photo,
        compound="left",
        command=lambda g=game: start_game(g)
    )
    btn.pack(fill="x", padx=10, pady=5)

root.mainloop()
