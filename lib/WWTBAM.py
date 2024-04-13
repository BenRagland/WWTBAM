import random
from models.question import Question
from models.game import *
from cli import *


ANSWER_OPTIONS = ['a', 'b', 'c', 'd', '1', '2', '3', '8']

def get_user_input(valid_input):
    """Get user input and check if it's valid"""
    while True:
        user_input = input("""Please enter a, b, c, or d \nOR \n
                           Enter 1 for Ask the Audience \n2 for Phone a Friend  \n3 for 50/50 \nOR \n
                           Enter 8 to Walk Away """)
        if user_input in valid_input:
            return user_input
        else: #If the input is invalid, print an error message.
            print("""Invalid input. Please enter a, b, c, or d \nOR \n
                  Enter 1, 2, or 3 to use a lifeline \nOR \n 
                  Enter 8 to Walk Away""")
            
def game_over():
    print(f'You walked away with {game.final_score}')
    print(f"Thanks for playing {cur_user.name}")
    
    """Prompt the player to either restart or quit the game"""
    choice = input("Would you like to restart the game (r), return to the main menu (m), or quit (q)?: "
                   ).lower()
    if choice == 'r':
        return play() #restart
    elif choice == 'q':
        return exit() #quit
    elif choice == 'm':
        return main()
    else: #If the input is invalid, print an error message.
        print("""Invalid input. Please enter 'r' to restart, 'q' to quit or 'm' 
              to return to the main menu.""")

def play():



    """Main method to run game"""
    questions = Question.all
    random.shuffle(questions) #TODO this needs better logic based on difficulty level
    game = Game.create(user_id=cur_user.id) #TODO global cur_user? how to get id - find or create method
    print(f"\nWelcome to WWTBAM {cur_user.name}!") #TODO make this better

    # Loop through questions list
    for index, question in enumerate(questions):
        print(f'\nFor {POINTS[index]}:')
        print(f"{question['question']}") #print the question

        # Randomise the order of options
        options = question.options
        random.shuffle(options)
        for j, option in enumerate(options):
            print(f"{ANSWER_OPTIONS[j]}. {option}") #print the options

        answer = get_user_input(ANSWER_OPTIONS) #get user input

        # If the answer is correct, update the player's score and print "Correct!"
        if answer == chr(97 + options.index(question['answer'])).lower():
            print("\nCorrect!")
            game.update_score(index)
        # elif:
            #TODO logic for lifelines
            #something about removing option from ANSWER_OPTIONS if life line is used

        elif answer == '8':
                print(f'\n You decided to walk away with {game.cur_score}.')
                game.cur_score = game.final_score
                game.update()
                game_over()
        else:
            # If the answer is incorrect, print "Incorrect!"
            print("\nIncorrect!")
            game_over()

        # Print player's current score
        print(f'Your total is now: {game.cur_score}')

    # Print the final score after all questions have been answered
    print(f"CONGRATULATIONS, {cur_user.name}!! You're a millionaire!")
    game_over()