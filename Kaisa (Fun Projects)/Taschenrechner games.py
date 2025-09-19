import random
import time
import sys
print("\n" * 100)
print("""
           _ _ _ _       _             
  ___ __ _| | (_) | __ _| |_ ___  _ __ 
 / __/ _` | | | | |/ _` | __/ _ \| '__|
| (_| (_| | | | | | (_| | || (_) | |   
 \___\__,_|_|_|_|_|\__,_|\__\___/|_|   """)
print("Tip: Whenever you need to enter an input, the valid options are shown in brackets after the question (e.g., 1, 2, 3, ...).\n")
def menu():
    games = ["Higher - Lower", "Blackjack","TicTacToe", "Program ende"]
    while True:
        for index, gameop in enumerate(games, start=1):
            print(index, gameop)
        sys.stdout.flush()
        choice = input("Wich game do you want to play?(1,2,...)")
        if choice == "1":
            HigherLower()
        elif choice == "2":
            Blackjack()
        elif choice == "3":
            TicTacToe()
        elif choice == "4":
            print("Program closes...")
            exit()
        else:
            print("not quite try entering on number corresponding to the games listed above for example '1' for Higher-Lower")
def HigherLower():
    """
    Starts the Higher-Lower guessing game where the player selects a difficulty,
    then tries to guess a randomly chosen number within the specified range.
    """

    def choosedifficulty():
        print("there are following difficulties:\n1. easy (0-10) \n2. mittelmäßig (0-100) \n3. Einstein (0-1000) \n4. Custom difficulty \n5. back to menu")
        while True:
            auswahl = input("What difficulty do you want to play on? (1, 2,...) ")
            if auswahl == "1":
                var1, var2 = 0, 10
                break
            elif auswahl == "2":
                var1, var2 = 0, 100
                break
            elif auswahl == "3":
                var1, var2 = 0, 1000
                break
            elif auswahl == "4":
                try:
                    var1 = int(input("please enter the lowest number: "))
                    var2 = int(input("please enter the higherst number: "))
                    if var1 >= var2:
                        print("the top number has to be bigger than the lowest")
                        continue
                    break
                except ValueError:
                    print("please enter a number")
            elif auswahl == "5":
                return
            else:
                print("not quite try entering on number corresponding to the options listed above for example '1' for easy")
        return var1, var2

    result = choosedifficulty()
    if result is None:
        return  # go back to menu if user selects option 5
    var1, var2 = result
    lösung = random.randint(var1, var2)
    var3 = 1

    while True:
        try:
            guess = int(input(f"What is your guess? (between {var1} and {var2}): "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if guess == lösung:
            print("wallah krass wp")
            print(f"you guessed correctly in {var3} tries")
            break
        elif guess < var1:
            print(f"the number should not be below {var1}")
        elif guess > var2:
            print(f"the number should not be above {var2}")
        else:
            if guess > lösung:
                print("lower!")
            elif guess < lösung:
                print("higher!")
            var3 += 1
    return


def Blackjack():
    print("Blackjack is a game in which")

def TicTacToe():
    def print_board(board):
        print("\n")
        for row in board:
            print(" | ".join(row))
            print("-" * 10)
        print("\n")

    def check_winner(board, player):
        for i in range(3):
            if all(field == player for field in board[i]) or all(board[j][i] == player for j in range(3)):
                return True
        # Diagonalen
        if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(board):
        return all(cell in ['X', 'O'] for row in board for cell in row)

    def get_move(player, board):
        while True:
            try:
                move = input(f"Spieler {player}, gib deine Position ein (1–9): ")
                pos = int(move) - 1
                if pos < 0 or pos > 8:
                    print("Bitte gib eine Zahl von 1 bis 9 ein.")
                    continue
                row, col = divmod(pos, 3)
                if board[row][col] in ['X', 'O']:
                    print("Dieses Feld ist schon belegt.")
                    continue
                return row, col
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

    def tiktaktoe():
        board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        current_player = "X"
        print_board(board)

        while True:
            row, col = get_move(current_player, board)
            board[row][col] = current_player
            print_board(board)

            if check_winner(board, current_player):
                print(f"🎉 Spieler {current_player} hat gewonnen!")
                break
            elif is_draw(board):
                print("🤝 Unentschieden!")
                break

            current_player = "O" if current_player == "X" else "X"

    tiktaktoe()

menu()