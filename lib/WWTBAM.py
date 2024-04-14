import random
from models.question import Question
from models.game import *
from cli import *

#TODO LET'S MAKE MOST OF THIS LOGIC HELPER FUNCTIONS

ANSWER_OPTIONS = ['a', 'b', 'c', 'd', '1', '2', '3', '8']
SAVE_POINTS = [25000, 1000]

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
            
def game_over(game):
    print(f'You walked away with {game.final_score}')
    print(f"Thanks for playing, {cur_user.name}")

    game.update()

    """Prompt the player to either restart or quit the game"""
    while True:
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

# Main method to run game
def play():

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
    random.shuffle(game_questions)

    game = Game.create(user_id=cur_user.id) #TODO global cur_user? how to get id - find or create method
    print(f"\nWelcome to WWTBAM {cur_user.name}!") #TODO make this better

    # Loop through 15 questions list
    for index, question in enumerate(game_questions):
        print(f'\nFor {POINTS[index]}:')
        print(f"{question.question}") #print the question

        # Randomise the order of options
        options = question.options
        random.shuffle(options)
        for j, option in enumerate(options):
            print(f"{ANSWER_OPTIONS[j]}. {option}") #print the options

        answer = get_user_input(ANSWER_OPTIONS) #get user input

        # If the answer is correct, update the player's score and print "Correct!"
        if answer == chr(97 + options.index(question.answer)).lower():
            print("\nCorrect!")
            game.update_score(index)

        elif answer == '1' and not ask_the_audience_used:
            ask_the_audience_used = True
            ANSWER_OPTIONS.remove('1')

            #TODO maybe add some actual math/logic here to render random amounts (majority for correct)
            print(f"The results are in! 60% of the audience thinks the answer is: {question.correct_answer}")
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
            answer = get_user_input(ANSWER_OPTIONS)

        elif answer == '3'and not fifty_fifty_used:
            fifty_fifty_used = True
            
            # Create a list of incorrect answers
            incorrect_answers = [option for option in options if option != question.correct_answer]
            
            # Randomly remove two incorrect answers
            two_incorrect_answers = random.sample(incorrect_answers, 2)
            for incorrect_answer in two_incorrect_answers:
                options.remove(incorrect_answer)
            
            # Print the remaining options
            for j, option in enumerate(options):
                print(f"{ANSWER_OPTIONS[j]}. {option}")
            
            # Get the user's answer again
            answer = get_user_input(ANSWER_OPTIONS)
        elif answer == '8':
                print(f'\n You decided to walk away with ${game.cur_score}.')
                game.final_score = game.cur_score
                game_over(game)
        else:
            print("\nI'm sorry, but that's incorrect!")
            for save_point in SAVE_POINTS:
                if game.cur_score >= save_point:
                    game.final_score = save_point
                    break
                else:
                    game.final_score = 0
            game_over(game)

        # Print player's current score
        print(f'Your total is now: ${game.cur_score}')

    # Print after all questions have been answered
    print(f"CONGRATULATIONS, {cur_user.name}!! You're a millionaire!")
    game.final_score = game.cur_score
    game_over(game)