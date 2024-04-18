# lib/cli.py
from cprint import cprint
import time

from helpers.helpers import (
    exit_program,
    get_user_high_score,
    get_all_high_scores

)
from models.users import Users
from models.question import Question
from models.game import Game
from WWTBAM import *
import os

#constant variable    
BANNER = """
WHO WANTS TO BE A...

███╗   ███╗██╗██╗     ██╗     ██╗ ██████╗ ███╗   ██╗ █████╗ ██╗██████╗ ███████╗██████╗ 
████╗ ████║██║██║     ██║     ██║██╔═══██╗████╗  ██║██╔══██╗██║██╔══██╗██╔════╝╚════██╗
██╔████╔██║██║██║     ██║     ██║██║   ██║██╔██╗ ██║███████║██║██████╔╝█████╗    ▄███╔╝
██║╚██╔╝██║██║██║     ██║     ██║██║   ██║██║╚██╗██║██╔══██║██║██╔══██╗██╔══╝    ▀▀══╝ 
██║ ╚═╝ ██║██║███████╗███████╗██║╚██████╔╝██║ ╚████║██║  ██║██║██║  ██║███████╗  ██╗   
╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝  ╚═╝
    """

cur_user = None

def main():
    os.system('clear')
    greeting()
    Users.create_table()
    Game.create_table()
    
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1": 
            global cur_user
            print("Enter your username:")
            username = input('> ')
            cur_user = Users.find_or_create_by(username.upper())
            print(f"Welcome, {cur_user.name}!")
        elif choice == '2':
            play(cur_user, main)
        elif choice == '3':
            #prints all games 
            if Game.get_games_by_user(cur_user.id):
                cprint("************************************************------     ALL GAMES PLAYED    ------************************************** \n ",c='c')
                for game in Game.get_games_by_user(cur_user.id):
                    cprint(game,c='y') 
            else:
                print('You haven\'t played any games yet!')
        elif choice == '4':
            get_user_high_score(cur_user.id)
        elif choice == '5':
            get_all_high_scores()
        elif choice == '6':
            Question.add_new_question()
        elif choice == '7':
            deleted = False
            validation = input(f"Are you sure you want to delete user {cur_user.name}? (Y/N)").upper()
            while deleted == False:
                if validation == "Y":
                    deleted == True
                    print(cur_user.id)
                    Users.delete_row(cur_user.id)
                    cur_user = None
                    main()
                elif validation == "N":
                    main()
                else:
                    print("Invalid response, please enter either Y or N.")
                    validation = input(f"Are you sure you want to delete user {cur_user.name}? (Y/N)")
        else:
            print("Invalid choice")
        

def menu():
    print("\nPlease select an option: \n")
    cprint("0. Exit the program", c='g')
    cprint("1. Enter/Change username", c='c')
    if (cur_user):
        cprint('2. Play New Game', c='y')
        cprint('3. See all games played', c='r')
        cprint('4. See my High Score', c='b')
        cprint('5. View all High Scores', c='m')
        cprint("6. Add a new question", c='c')  
        cprint('7. Delete Current User', c='g')

def greeting():
    for char in BANNER:
        cprint(char, end='', flush=True, c='m')
        time.sleep(0.005)

if __name__ == "__main__":
    main()
    
    
