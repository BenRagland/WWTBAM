# lib/cli.py
from cprint import cprint
import time
from seed.question_seed import seed_questions
from helpers.helpers import (
    exit_program,
    list_users,
    find_user_by_name,
    update_user,
    get_user_high_score,
    get_all_high_scores

)
from models.users import Users
from models.question import Question
from models.game import Game
from WWTBAM import *


cur_user = None

# populate questions table with seed data
def populate_default_questions():
    Question.drop_table()
    Question.create_table()

    #Create The Question Objs
    for item in seed_questions:
        Question(*item)

    # #Create rows in questions table with each Obj
    # [obj.create_row() for obj in question_objs_list]
    

def main():
    
    Users.create_table()
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
            if Game.get_games_by_user(cur_user.id):
                print(Game.get_games_by_user(cur_user.id)) 
            else:
                print('You haven\'t played any games yet!')
        elif choice == '3':
            get_user_high_score(cur_user.id)
            # print(f"Your high score: {user_high_score}")
        elif choice == '4':
            play(cur_user)
        elif choice == '5':
            get_all_high_scores()
        elif choice == '6':
            #TODO add an "are you sure?"
            Users.delete_row(cur_user.id)
            cur_user = None
        else:
            print("Invalid choice")
#wait til errthang is finished and do menu all together?

def menu():
    print("Please select an option:")
    cprint("0. Exit the program", c='g')
    cprint("1. Enter/Change username", c='c')
    if (cur_user):
        cprint('2. See all games played', c='y')
        cprint('3. See my High Score', c='r')
        cprint('4. Play New Game', c='b')
        cprint('5. View all High Scores', c='m')
        cprint('6. Delete Current User', c='g')


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

# def greeting():
#     # cprint(BANNER, c='m')
#     for kk in range(len(BANNER)):
#         print(BANNER[0:kk+1+1], end = '\r')
#         time.sleep(0.1)
#     #add more greeting

def greeting():
    for char in BANNER:
        cprint(char, end='', flush=True, c='m')
        time.sleep(0.005)

if __name__ == "__main__":
    greeting()
    main()
    
    
