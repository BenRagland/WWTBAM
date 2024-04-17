import random
from models.question import Question
from seed.question_seed import seed_questions
from models.game import *
import os
import time
from helpers.WWTBAM_helpers import *

#TODO LET'S MAKE MOST OF THIS LOGIC HELPER FUNCTIONS

ANSWER_OPTIONS = ['a', 'b', 'c', 'd', '1', '2', '3', '8']
SAVE_POINTS = [25000, 1000]

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
               ask_the_audience(ANSWER_OPTIONS, question, options, phone_a_friend_used, fifty_fifty_used)
        
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