# lib/helpers.py
from models.users import Users


def helper_1():
    print("Performing useful function#1.")

def list_users():
    users = Users.get_all()
    for user in users: 
        print(user)
        
def find_user_by_id():
    #use a trailing underscore not to override the built-in id function
    id_ = input("Enter the user id: ")
    user = Users.find_by_id(id_)            
    print(user) if user else print(f'User {id_} not found')
        
def find_user_by_name():
    name = input("Enter the user name: ")
    user = Users.find_by_name(name)          
    
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
            
# Retrieve the high score for the specified user ID
# Print and return user's high score
def get_user_high_score(user_id):
    high_score = Users.get_user_high_score(user_id)
    print(f"Your high score: {high_score}")
    return high_score

# Retrieve all high scores
# Check if high scores exist, iterate over each high score, and find user with the given user_id
# Check if user exists, then print users name and high score
def get_all_high_scores():
    all_high_scores = Users.get_all_high_scores()
    if all_high_scores:
        for user_id, user_name, high_score in all_high_scores:
            user = Users.find_by_id(user_id)
            if user:
                print(f"User: {user_name}, High Score: {high_score}")
            else:
                print(f"No user found with ID: {user_id}")
    else:
        print("No high scores found.")

def exit_program():
    print("Goodbye!")
    exit()

