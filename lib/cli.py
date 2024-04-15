# lib/cli.py

from helpers.helpers import (
    exit_program,
    list_users,
    find_user_by_name,
    update_user

)
from models.users import Users
from models.question import Question
from models.game import Game
from WWTBAM import *


cur_user = None

def main():
    Users.create_table()
    Question.create_table()
    Game.create_table()

    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1": #TODO set cur_user (global)
            global cur_user
            print("Enter your username:")
            username = input('> ')
            cur_user = Users.find_or_create_by(username.upper())
            print(f"Welcome, {cur_user.name}!")
        elif choice == '2':
            #prints all games 
            print(Users.get_games_by_user(cur_user.id)) 
        elif choice == '3':
            pass
        elif choice == '4':
        # else:
            print("Invalid choice")
#wait til errthang is finished and do menu all together?

def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Enter/Change username")
    if (cur_user):
        print('2. See all games played')
        print('3. See my High Score')
        print('4. Play New Game')
        print('5. Delete Current User')


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

def greeting():
    print(BANNER)
    #add more greeting



if __name__ == "__main__":
    main()
