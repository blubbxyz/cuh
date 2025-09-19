import random
import os
import msvcrt

def menue():
    os.system("cls")
    print("Welcome to Number Guessing with a Twist!")
    while True:
        help = input("Do you need an explanation of the game's rules? yes(1)/no(2): ")
        if help == "1":
            print(
                "In this game, you will guess a random number within a specified range.\n"
                "The game will provide feedback on whether your guess is too high or too low.\n"
                "You can choose from three difficulty levels: Easy (0-30), Medium (0-100), and Hard (0-1000).\n"
                "The game will continue until you guess the correct number.\n"
            )
            input("Press Enter to continue...")
            break
        elif help == "2":
            break
        else:
            print("Please choose either 1 or 2.")
    difficulty = choose_difficulty()
    game(difficulty)

def choose_difficulty():
    options = ["easy", "medium", "hard"]
    idx = 0
    while True:
        os.system("cls")
        print("Choose difficulty (w/s and Enter):\n")
        for i, opt in enumerate(options):
            if i == idx:
                print(f"> {opt.upper()} <")
            else:
                print(f"  {opt}  ")
        key = msvcrt.getch()
        if key.isascii():
            key = key.decode()

        
            if key == "s":
                idx = (idx + 1) % len(options)
            elif key == "w":
                idx = (idx - 1) % len(options)
            elif key == "\r":
                return options[idx]

def game(difficulty):
    if difficulty == "easy":
        start, end = 0, 30
    elif difficulty == "medium":
        start, end = 0, 100
    elif difficulty == "hard":
        start, end = 0, 1000

    number = random.randint(start, end)
    attempts = 0

    while True:
        try:
            guess = int(input(f"Guess a number between {start} and {end}: "))
            attempts += 1
            if guess < number:
                print("Too low!")
            elif guess > number:
                print("Too high!")
            else:
                print(f"Correct! The number was {number}. You guessed it in {attempts} tries.")
                break
        except ValueError:
            print("Please enter a valid number.")

menue()
