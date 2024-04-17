import random
from models.question import Question
from seed.question_seed import seed_questions
from models.game import *
import os
import time

#constants for the game 
ANSWER_OPTIONS = ['a', 'b', 'c', 'd', '1', '2', '3', '8'] #list of valid answers
#if user gets 1000 points or 25000 points, and get a question wrong they can't get less than that
SAVE_POINTS = [25000, 1000]

#constants for get_user_input
ask_the_audience_used = False
phone_a_friend_used = False
fifty_fifty_used = False

# populate questions table with seed data
def populate_default_questions():
    Question.all.clear()
    Question.drop_table()
    Question.create_table()

    #Create The Question Objs
    for item in seed_questions:
        Question(*item)

def get_user_input(valid_input):
    """Get user input and check if it's valid"""
    while True:
        options_text = "\nPlease enter a, b, c, or d"
        if '1' in valid_input and not ask_the_audience_used:
            options_text += "\n1 for Ask the Audience"
        if '2' in valid_input and not phone_a_friend_used:
            options_text += "\n2 for Phone a Friend"
        if '3' in valid_input and not fifty_fifty_used:
            options_text += "\n3 for 50/50"
        options_text += "\nOR\nEnter 8 to Walk Away\n>"
        user_input = input(options_text)
        if user_input in valid_input:
            return user_input
        else: #If the input is invalid, print an error message.
            print("Invalid input.")
            print(options_text)
            
def game_over(game, cur_user, main_callback):
    print(f'You walked away with ${game.final_score}')
    print(f"Thanks for playing, {cur_user.name}")
    #TODO Add User class method to get/update user high score after each game is played
    game.update()

    old_high_score = Users.get_user_high_score(game.user_id)
    if game.final_score > old_high_score:
        Users.update_high_score(game.final_score, game.user_id)
    print(old_high_score)
    print(game.final_score)

    """Prompt the player to either restart or quit the game"""
    while True:
        choice = input("Would you like to restart the game (r), return to the main menu (m), or quit (q)?: "
                    ).lower()
        if choice == 'r':
            return play(cur_user, main_callback) #restart
        elif choice == 'q':
            return exit() #quit
        elif choice == 'm':
            return main_callback()
        else: #If the input is invalid, print an error message.
            print("""Invalid input. Please enter 'r' to restart, 'q' to quit or 'm' 
                to return to the main menu.""")

# Main method to run game
def play(cur_user, main_callback):
    os.system('clear')
    game = Game.create(user_id = cur_user.id)
    populate_default_questions()

    ask_the_audience_used = False
    phone_a_friend_used = False
    fifty_fifty_used = False
    
    #resetting answer options at the start of a new game
    ANSWER_OPTIONS = ['a', 'b', 'c', 'd', '1', '2', '3', '8']

    questions = Question.all

    # Shuffle the questions, but keep the difficulty levels separate
    #? Should these be class methods??
    easy_questions = [question for question in questions if question.difficulty == "Easy"]
    medium_questions = [question for question in questions if question.difficulty == "Medium"]
    hard_questions = [question for question in questions if question.difficulty == "Hard"]

    random.shuffle(easy_questions)
    random.shuffle(medium_questions)
    random.shuffle(hard_questions)

    game_questions = easy_questions[:5] + medium_questions[:5] + hard_questions[:5]
 
    print(f"\nWelcome to WWTBAM, {cur_user.name}!") #TODO make this better

    # Loop through 15 questions list
    for index, question in enumerate(game_questions): 
         # Print player's current score
        print(f'Your total is now: ${game.cur_score}')
        print(f'\nFor ${POINTS[index]}:')
        print(f"{question.question}") #print the question

        # Randomise the order of options
        options = question.answers
        random.shuffle(options)
        for j, option in enumerate(options):
            print(f"{ANSWER_OPTIONS[j]}. {option}") #print the options

        answer = get_user_input(ANSWER_OPTIONS, ask_the_audience_used, phone_a_friend_used, fifty_fifty_used) #get user input
        answered = False
        #control flow of user input either answer or lifeline option
        # If the answer is correct, update the player's score and print "Correct!"
        while not answered:
            if answer == chr(97 + options.index(question.correct_answer)).lower(): 
                answered = True
                print("\nCorrect!")
                game.update_score(index)
                time.sleep(1)
                os.system('clear')

            elif answer == '1' and not ask_the_audience_used:
                ask_the_audience_used = True
                ANSWER_OPTIONS.remove('1')

                #TODO maybe add some actual math/logic here to render random amounts (majority for correct)
                print(f"The results are in! 60% of the audience thinks the answer is: {question.correct_answer}")
                print(f"{question.question}")
                for j, option in enumerate(options):
                    print(f"{ANSWER_OPTIONS[j]}. {option}")
                answer = get_user_input(ANSWER_OPTIONS)
        
            elif answer == '2' and not phone_a_friend_used:
                phone_a_friend_used = True
                ANSWER_OPTIONS.remove('2')

                correct_answer_probability = 0.8  # 80% chance of getting the correct answer
                if random.random() < correct_answer_probability: #random.random() generates a float between 0.0 and 1.0
                    print(f"""Hi, {cur_user.name}! Thanks for calling me! I'm gonna have to say the 
                    correct answer is: {question.correct_answer}""")
                else:
                    wrong_answers = [answer for answer in question.answers if answer != question.correct_answer]
                    print(f"""Hi, {cur_user.name}! Thanks for calling me! Uh, I think I'm gonna have to say 
                    the correct answer is: {random.choice(wrong_answers)}""")
                print(f"{question.question}")
                for j, option in enumerate(options):
                    print(f"{ANSWER_OPTIONS[j]}. {option}")
                answer = get_user_input(ANSWER_OPTIONS, ask_the_audience_used, phone_a_friend_used, fifty_fifty_used)

            elif answer == '3'and not fifty_fifty_used:
                fifty_fifty_used = True
                ANSWER_OPTIONS.remove('3')

                options_copy = options.copy()
                # Create a list of incorrect answers
                incorrect_answers = [option for option in options_copy if option != question.correct_answer]
                
                # Randomly remove two incorrect answers
                two_incorrect_answers = random.sample(incorrect_answers, 2)
                for incorrect_answer in two_incorrect_answers:
                    options_copy.remove(incorrect_answer)
                
                print(f"{question.question}")
                # Print the remaining options
                for j, option in enumerate(options_copy):
                    print(f"{ANSWER_OPTIONS[j]}. {option}")
                
                # Get the user's answer again
                answer = get_user_input(ANSWER_OPTIONS, ask_the_audience_used, phone_a_friend_used, fifty_fifty_used)

                if answer == chr(97 + options_copy.index(question.correct_answer)).lower():
                    answered = True
                    print("\nCorrect!")
                    game.update_score(index)
                    time.sleep(1)
                    os.system('clear')
                else:
                    print("\nI'm sorry, but that's incorrect!")
                    for save_point in SAVE_POINTS:
                        if game.cur_score >= save_point:
                            game.final_score = save_point
                            break
                        else:
                            game.final_score = 0
                    game_over(game, cur_user, main_callback)
            elif answer == '8':
                    print(f'\nYou decided to walk away.')
                    game.final_score = game.cur_score
                    return game_over(game, cur_user, main_callback, play)
            else:
                print("\nI'm sorry, but that's incorrect!")
                for save_point in SAVE_POINTS:
                    if game.cur_score >= save_point:
                        game.final_score = save_point
                        break
                    else:
                        game.final_score = 0
                game_over(game, cur_user, main_callback, play)

    # Print after all questions have been answered
    print(f"CONGRATULATIONS, {cur_user.name}!! You're a millionaire!")
    game.final_score = game.cur_score
    game_over(game, cur_user, main_callback, play)