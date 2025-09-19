
import os
import keyboard

def arrow_menu_vertical(title, options):
    """
    Displays a vertical menu using ↑ ↓ and Enter.
    :param title: Menu title (e.g. "Choose an option:")
    :param options: List of selectable options
    :return: The selected option (as a string)
    """
    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(title + "\n")
        for i, opt in enumerate(options):
            if i == idx:
                print(f"> {opt.upper()} <")  # Highlighted option
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

import os
import keyboard

def arrow_menu_horizontal(title, options):
    """
    Displays a horizontal menu using ← → and Enter.
    :param title: Menu title (e.g. "Choose a difficulty:")
    :param options: List of selectable options
    :return: The selected option (as a string)
    """
    idx = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(title + "\n")

        # Display all options side by side
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

def main():
    difficulty = arrow_menu_horizontal("Select Difficulty:", ["easy", "medium", "hard"])
    print(f"You selected: {difficulty}")

if __name__ == "__main__":
    main()
