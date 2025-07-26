# Rock-Paper-Scissors(-Lizard-Spock) Terminal Game
# Developed by Sidhanshi1820 as an Internship Project
# Enhanced by GitHub Copilot

import random
import sys
import time
import os
from datetime import datetime

# ANSI color codes for output
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_MAGENTA = "\033[95m"
COLOR_BLUE = "\033[94m"
COLOR_WHITE = "\033[97m"

WIN_MSGS = [
    "You win! 🎉", "Great job!", "Victory is yours!",
    "Awesome win!", "You rocked it!", "You're on fire! 🔥"
]
LOSE_MSGS = [
    "Computer wins! 😅", "Oops, lost this round.", "Better luck next time!",
    "The computer got you!", "Don't give up!", "Try again!"
]
TIE_MSGS = [
    "It's a tie! 😮", "Draw!", "Nobody wins this round.",
    "So close! Try again.", "Dead heat!"
]

ASCII_ART_TITLE = COLOR_MAGENTA + r"""
  ______            _              _____                                      
 | ___ \          | |            /  ___|                                     
 | |_/ /___  _   _| | ___   _   \ `--.  ___ __ _ _ __  _ __   ___ _ __       
 |    // _ \| | | | |/ / | | |   `--. \/ __/ _` | '_ \| '_ \ / _ \ '__|      
 | |\ \ (_) | |_| |   <| |_| |  /\__/ / (_| (_| | | | | | | |  __/ |         
 \_| \_\___/ \__,_|_|\_\\__, |  \____/ \___\__,_|_| |_|_| |_|\___|_|         
                        __/ |                                                
                       |___/             
""" + COLOR_RESET

def beep():
    """Play a beep sound (works in most terminals)."""
    try:
        if os.name == 'nt':
            import winsound; winsound.Beep(1000, 150)
        else:
            print('\a', end='', flush=True)
    except Exception:
        pass

def clear_screen():
    """Clear the terminal screen for a 'game' experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(message, delay=0.01):
    """Type out a message like a typewriter for better UX."""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading_screen():
    clear_screen()
    print(ASCII_ART_TITLE)
    print(COLOR_CYAN + "Loading", end='')
    for _ in range(5):
        print(".", end='', flush=True)
        time.sleep(0.3)
    print(COLOR_RESET)
    time.sleep(0.5)
    clear_screen()

def confetti():
    """Display a celebratory confetti effect."""
    for i in range(3):
        print(COLOR_MAGENTA + "✨🎉✨" + COLOR_YELLOW + "   Congratulations!   " + COLOR_GREEN + "✨🎉✨" + COLOR_RESET)
        time.sleep(0.2)
    print()

def print_header():
    """Print the ASCII art header."""
    clear_screen()
    print(ASCII_ART_TITLE)

def get_user_choice(choices, advanced):
    """Prompt the user for their move. Handles help/rules commands."""
    abbr_map = {c[0]: c for c in choices}
    prompt = f"Choose your move ({'/'.join([f'{c[0]}:{c}' for c in choices])}): "
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == "help":
            show_help(advanced)
            continue
        if user_input == "rules":
            show_rules(advanced)
            continue
        if user_input == "exit":
            print(COLOR_MAGENTA + "\nExiting this round. See you soon!" + COLOR_RESET)
            return "exit"
        if user_input in choices:
            return user_input
        elif user_input in abbr_map:
            return abbr_map[user_input]
        print(COLOR_YELLOW + "Invalid input. Try again (type 'help' for options)." + COLOR_RESET)

def get_computer_choice(choices):
    """Random computer move with suspense."""
    print("Computer is thinking", end='', flush=True)
    for _ in range(3):
        print(".", end='', flush=True)
        time.sleep(0.4)
    print()
    return random.choice(choices)

def determine_winner(user, computer, beats_map):
    """Return winner: 'user', 'computer', or 'tie'."""
    if user == computer:
        return "tie"
    elif computer in beats_map[user]:
        return "user"
    else:
        return "computer"

def display_result(user, computer, winner):
    """Display round result and a random message."""
    print(f"\nYou chose:      {COLOR_BOLD}{user.capitalize()}{COLOR_RESET}")
    print(f"Computer chose: {COLOR_BOLD}{computer.capitalize()}{COLOR_RESET}")
    beep()
    if winner == "tie":
        print(COLOR_YELLOW + random.choice(TIE_MSGS) + COLOR_RESET)
    elif winner == "user":
        print(COLOR_GREEN + random.choice(WIN_MSGS) + COLOR_RESET)
    else:
        print(COLOR_RED + random.choice(LOSE_MSGS) + COLOR_RESET)

def play_again():
    """Prompt to play another round."""
    while True:
        again = input(COLOR_CYAN + "\nDo you want to play another round? (yes/no): " + COLOR_RESET).lower().strip()
        if again in ['yes', 'y']:
            return True
        elif again in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'.")

def show_rules(advanced=False):
    """Display the game rules."""
    print(COLOR_MAGENTA + "\nGame Rules:")
    if not advanced:
        print("- Rock beats Scissors")
        print("- Scissors beats Paper")
        print("- Paper beats Rock")
    else:
        print("- Scissors cuts Paper")
        print("- Paper covers Rock")
        print("- Rock crushes Lizard")
        print("- Lizard poisons Spock")
        print("- Spock smashes Scissors")
        print("- Scissors decapitates Lizard")
        print("- Lizard eats Paper")
        print("- Paper disproves Spock")
        print("- Spock vaporizes Rock")
        print("- Rock crushes Scissors")
    print(COLOR_RESET)

def show_help(advanced=False):
    """Display help message."""
    print(COLOR_WHITE + COLOR_BOLD + "\nGame Help:")
    c = ['rock', 'paper', 'scissors']
    if advanced:
        c.extend(['lizard', 'spock'])
    print(f"- Moves: {', '.join(c)}")
    print("- You can type the full name or just the first letter (e.g., 'r' for rock).")
    print("- Type 'rules' to see the rules.")
    print("- Type 'help' to see this help message.")
    print("- Type 'exit' to end this round early.\n" + COLOR_RESET)

def print_stats(user_score, computer_score, ties, history, start_time, player_name):
    """Print and save game statistics."""
    total_played = user_score + computer_score + ties
    elapsed = time.time() - start_time
    mins, secs = divmod(int(elapsed), 60)
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    summary = []
    print("\n" + "="*40)
    print("Game Statistics:")
    print(f"Player:        {COLOR_CYAN}{player_name}{COLOR_RESET}")
    print(f"Session Start: {COLOR_CYAN}{dt}{COLOR_RESET}")
    print(f"Total rounds played: {total_played}")
    print(f"Your Wins:     {COLOR_GREEN}{user_score}{COLOR_RESET}")
    print(f"Computer Wins: {COLOR_RED}{computer_score}{COLOR_RESET}")
    print(f"Ties:          {COLOR_YELLOW}{ties}{COLOR_RESET}")
    print(f"Elapsed time:  {COLOR_CYAN}{mins}m {secs}s{COLOR_RESET}")
    if total_played:
        win_percent = (user_score / total_played) * 100
        print(f"Your win percentage: {win_percent:.1f}%")
    print("Round History:")
    for i, (u, c, res) in enumerate(history, 1):
        col = COLOR_GREEN if res == "user" else COLOR_RED if res == "computer" else COLOR_YELLOW
        outcome = 'You win' if res == 'user' else 'Computer wins' if res == 'computer' else 'Tie'
        print(f"  Round {i}: You - {u.capitalize()}, Computer - {c.capitalize()} => {col}{outcome}{COLOR_RESET}")
        summary.append(f"Round {i}: You - {u.capitalize()}, Computer - {c.capitalize()} => {outcome}")
    print("="*40)
    # Save to file
    try:
        with open("game_summary.txt", "a", encoding="utf-8") as f:
            f.write(f"\nSession: {dt} | Player: {player_name}\n")
            f.write(f"Total played: {total_played}, Your Wins: {user_score}, Computer Wins: {computer_score}, Ties: {ties}, Time: {mins}m{secs}s\n")
            f.write("History:\n")
            for line in summary:
                f.write(line + "\n")
            f.write("="*40 + "\n")
    except Exception as e:
        print(COLOR_RED + f"Error saving summary: {e}" + COLOR_RESET)

def mode_selection():
    """Prompt for mode selection."""
    while True:
        mode_input = input("Type 'advanced' for Lizard-Spock mode, 'rules' for rules, or press Enter for classic: ").strip().lower()
        if mode_input == 'advanced':
            return True
        elif mode_input == 'rules':
            show_rules(advanced=False)
        elif mode_input == '':
            return False
        else:
            print(COLOR_YELLOW + "Invalid input. Please try again." + COLOR_RESET)

def rounds_selection():
    """Prompt for number of rounds."""
    while True:
        rounds_input = input("Enter number of rounds to play (leave blank for endless mode): ").strip()
        if rounds_input == '':
            print("Endless mode: play as many rounds as you like.\n")
            return None
        elif rounds_input.isdigit() and int(rounds_input) > 0:
            print(f"Best of {rounds_input} rounds enabled.\n")
            return int(rounds_input)
        else:
            print(COLOR_YELLOW + "Please enter a positive integer or leave blank." + COLOR_RESET)

def best_of_win(user_score, computer_score, total_rounds):
    """Check if either player has clinched a best-of-N series."""
    needed = (total_rounds // 2) + 1
    return user_score >= needed or computer_score >= needed

def get_player_name():
    """Prompt for and sanitize player name."""
    while True:
        name = input(COLOR_CYAN + "Enter your name: " + COLOR_RESET).strip()
        if not name:
            print(COLOR_YELLOW + "Name cannot be empty. Please enter a valid name." + COLOR_RESET)
            continue
        if any(c in name for c in r'\/:*?"<>|'):
            print(COLOR_YELLOW + "Name cannot contain special characters: \\ / : * ? \" < > |" + COLOR_RESET)
            continue
        return name

def main_menu():
    """Show main menu and get user selection."""
    print(COLOR_BOLD + COLOR_MAGENTA + "\nWelcome to the main menu!" + COLOR_RESET)
    print("1. Play Game")
    print("2. View Past Game Summaries")
    print("3. Help")
    print("4. Exit")
    while True:
        choice = input(COLOR_CYAN + "Select an option (1-4): " + COLOR_RESET).strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print(COLOR_YELLOW + "Invalid input. Please enter 1, 2, 3, or 4." + COLOR_RESET)

def view_past_summaries():
    """Display previous game summaries."""
    print(COLOR_BOLD + COLOR_WHITE + "\n--- Previous Game Summaries ---" + COLOR_RESET)
    try:
        with open("game_summary.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print(COLOR_YELLOW + "No past summaries found. Play a game to create one!" + COLOR_RESET)
    except Exception as e:
        print(COLOR_RED + f"Error reading summaries: {e}" + COLOR_RESET)

def play_game():
    """Main game loop with all enhancements."""
    while True:
        loading_screen()
        print_header()
        typewriter("Welcome to the ultimate Rock-Paper-Scissors game!")
        player_name = get_player_name()
        print("Instructions:")
        print(" - Type 'rock', 'paper', or 'scissors' (or 'r', 'p', 's').")
        print(" - Type 'advanced' for Lizard-Spock mode.")
        print(" - At any time, type 'help' or 'rules' or 'exit'.\n")
        
        user_score = 0
        computer_score = 0
        ties = 0
        round_num = 1
        history = []
        start_time = time.time()
        try:
            advanced = mode_selection()
            choices = ['rock', 'paper', 'scissors']
            beats_map = {
                'rock': ['scissors'],
                'paper': ['rock'],
                'scissors': ['paper']
            }
            if advanced:
                choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
                beats_map = {
                    'rock': ['scissors', 'lizard'],
                    'paper': ['rock', 'spock'],
                    'scissors': ['paper', 'lizard'],
                    'lizard': ['spock', 'paper'],
                    'spock': ['scissors', 'rock'],
                }
                print(COLOR_BOLD + "Advanced mode enabled! Choices are: rock, paper, scissors, lizard, spock.\n" + COLOR_RESET)
            rounds = rounds_selection()

            show_rules(advanced=advanced)
            input(COLOR_CYAN + "\nPress Enter to start the game!" + COLOR_RESET)

            while True:
                print_header()
                print(COLOR_BLUE + f"\n=== Round {round_num} ===" + COLOR_RESET)
                print(f"{COLOR_CYAN}Current Score — {player_name}: {user_score}, Computer: {computer_score}, Ties: {ties}{COLOR_RESET}")
                user_choice = get_user_choice(choices, advanced)
                if user_choice == "exit":
                    print(COLOR_MAGENTA + "\nYou exited the round early." + COLOR_RESET)
                    break
                computer_choice = get_computer_choice(choices)
                winner = determine_winner(user_choice, computer_choice, beats_map)
                display_result(user_choice, computer_choice, winner)
                history.append((user_choice, computer_choice, winner))

                if winner == "user":
                    user_score += 1
                elif winner == "computer":
                    computer_score += 1
                else:
                    ties += 1

                print(f"\n{COLOR_GREEN}{player_name}{COLOR_RESET}: {user_score} - {COLOR_RED}Computer{COLOR_RESET}: {computer_score} - {COLOR_YELLOW}Ties: {ties}{COLOR_RESET}")

                # Pause for suspense
                time.sleep(1.1)

                # Check for win in 'best of' mode, or if all rounds played
                if rounds is not None and (best_of_win(user_score, computer_score, rounds) or round_num == rounds):
                    print(COLOR_BOLD + "\nGame Over (Best of series reached)!" + COLOR_RESET)
                    break
                if not play_again():
                    break
                round_num += 1

            print_stats(user_score, computer_score, ties, history, start_time, player_name)

            # Celebration!
            if user_score > computer_score:
                confetti()
                print(COLOR_GREEN + "You are the overall winner! Congratulations!" + COLOR_RESET)
            elif user_score < computer_score:
                print(COLOR_RED + "Computer wins overall. Better luck next time!" + COLOR_RESET)
            else:
                print(COLOR_YELLOW + "It's an overall tie!" + COLOR_RESET)

            print(COLOR_CYAN + "\nThank you for playing Rock-Paper-Scissors!\n" + COLOR_RESET)
            # Ask if the user wants to play again, change mode, or exit
            while True:
                print(COLOR_WHITE + "\nChoose an option:\n 1. Play again (same mode)\n 2. Change mode\n 3. Main Menu\n 4. Exit" + COLOR_RESET)
                opt = input("Enter your choice (1/2/3/4): ").strip()
                if opt == "1":
                    break
                elif opt == "2":
                    return play_game()  # Recursively call for mode change
                elif opt == "3":
                    return  # Back to main menu
                elif opt == "4":
                    print(COLOR_MAGENTA + "\nGoodbye!" + COLOR_RESET)
                    sys.exit()
                else:
                    print(COLOR_YELLOW + "Invalid input. Please enter 1, 2, 3, or 4." + COLOR_RESET)
        except KeyboardInterrupt:
            print(COLOR_MAGENTA + "\n\nSession interrupted. Saving summary and exiting. Goodbye!" + COLOR_RESET)
            print_stats(user_score, computer_score, ties, history, start_time, player_name)
            sys.exit()

def help_screen():
    """Display help/instructions."""
    print(COLOR_BOLD + COLOR_CYAN + "\n--- Help & Instructions ---" + COLOR_RESET)
    print("This is a terminal-based Rock-Paper-Scissors game with an optional advanced mode (Lizard-Spock).")
    print("Features:")
    print("- Classic and advanced modes.")
    print("- Play for a set number of rounds or in endless mode.")
    print("- Detailed stats and session summaries.")
    print("- Type 'help', 'rules', or 'exit' at any prompt for assistance.")
    print("- Your game summaries are saved in 'game_summary.txt'.")
    print("- Celebrate your overall win with confetti!\n")

if __name__ == "__main__":
    while True:
        loading_screen()
        print_header()
        choice = main_menu()
        if choice == "1":
            play_game()
        elif choice == "2":
            view_past_summaries()
            input(COLOR_CYAN + "\nPress Enter to return to menu..." + COLOR_RESET)
        elif choice == "3":
            help_screen()
            input(COLOR_CYAN + "\nPress Enter to return to menu..." + COLOR_RESET)
        elif choice == "4":
            print(COLOR_MAGENTA + "\nThanks for playing! Goodbye!" + COLOR_RESET)
            sys.exit()