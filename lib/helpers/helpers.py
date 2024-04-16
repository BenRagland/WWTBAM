# lib/helpers.py
from models.users import Users
from models.game import Game

def helper_1():
    print("Performing useful function#1.")

def list_users():
    users = Users.get_all()
    for user in users: 
        print(user)
        
def find_user_by_id():
    #use a trailing underscore not to override the built-in id function
    id_ = input("Enter the user id: ")
    user = Users.find_by_id(id_)            ### WRITE THIS AS CLASS METHOD IN USER CLASS @classmethod find_by_id
    print(user) if user else print(f'User {id_} not found')
        
def find_user_by_name():
    name = input("Enter the user name: ")
    user = Users.find_by_name(name)          ### WRITE THIS METHOD IN USER class @classmethod find_by_name
    
def update_user():
    id_ = input("Enter the user id: ")
    if user := Users.find_by_id(id_):
        try: 
            name = input("Enter the user's new name: ")
            user.name = name
            
            user.update()
            print(f'Success: {user}')
        except Exception as exc:
            print("Error updating user name: ", exc)
        else:
            print(f'User {id_} not found')
            
# def delete_user():
#     id_ = input("Enter the user's name: ")
#     if user := Users.find_by_name
    

def get_user_high_score(user_id):
    high_score = Game.get_user_high_score(user_id)
    print(f"user ID {user_id} high score: {high_score}")
    return high_score

def get_all_high_scores():
    all_high_scores = Game.get_all_high_scores()
    for user_id, high_score in all_high_scores:
        print(f"user ID {user_id} high score: {high_score}")
    return all_high_scores

def exit_program():
    print("Goodbye!")
    exit()

