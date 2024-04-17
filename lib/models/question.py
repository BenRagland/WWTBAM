#lib/models/question.py
import sqlite3
import pickle
from seed.question_seed import seed_questions


CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Question:
    
    #list of objects saved to the database
    all = []
        
        
    #constructor to initialize Question object
    def __init__(self, question="", answers = None, correct_answer="", difficulty={}, id=None):
        self.question = question 
        self.answers = answers
        self.correct_answer = correct_answer
        self.difficulty = difficulty['difficulty']
        self.id = id
        type(self).all.append(self)
        self.save()

    #getter and setter for answers property
    @property
    def answers(self):
        return self._answers
    
    @answers.setter
    def answers(self, answers):
        if answers is None:
            self._answers = []
        elif isinstance(answers, list) and len(answers) == 4:
            self._answers = answers
        else:
            raise Exception("Answers should be a list of 4 answers")
        
    # Method to create the 'questions' table if it doesn't exist      
    @classmethod
    def create_table(cls):
        """create a new table to persist the attributes of the question instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answers TEXT,
                correct_answer TEXT,
                difficulty BLOB);
                """
        CURSOR.execute(sql)
        CONN.commit()


    # Method to save the Question instance to the database
    def save(self):
        db_answers = pickle.dumps(self.answers)
        db_difficulty = pickle.dumps(self.difficulty)

        try:
            sql="""
                    INSERT INTO questions (question, answers, correct_answer, difficulty) VALUES (?,?,?,?);
                """
            CURSOR.execute(sql,(self.question, db_answers, self.correct_answer, db_difficulty))
            self.id = CURSOR.lastrowid
            CONN.commit()
           
        except Exception as err:
            print(f'Save went wrong,{err}')
            
    
    # Method to create a new row in the 'questions' table // creates a new question
    @classmethod
    def create_row(cls,question,answer,correct_answer,difficulty):
        newQuestion = cls(question,answer,correct_answer,difficulty)
        newQuestion.save()
        return newQuestion
    
    # Method to delete a row from the 'questions' table by id // deletes a question
    @classmethod
    def del_row(cls,id):
        try:
            sql = """
                    DELETE FROM questions WHERE id = ?;
                """
            CURSOR.execute(sql,(id,))
            CONN.commit()
            print(f"Success!! Deleted row of  id:{id}")
        except Exception as err:
            print(f"Error Deleting {id} error:{err}")
    
    # Method to drop the 'questions' table // destructive operation to delete all questions from database
    # would only be used during development or if resetting the database schema
    @classmethod
    def drop_table(cls):
        sql=""" DROP TABLE IF EXISTS questions; """
        CURSOR.execute(sql)
        CONN.commit()
    
    def __repr__(self):
        return f'Question: {self.question}'

    # Static method to add a new question through the CLI
    # ** Static methods are designed to be utility or helper functions that perform tasks at the class level,
    #    not tied to any specific object instance. They operate on input parameters
    # ** Used a static method because it doesnt depend on any instance or class variables // operates independently to 
    #    create a new question without modifying any class-level variables or methods
    @staticmethod
    def add_new_question():
        print("Please enter the details for the new question: ")
        question_text = input("Question: ")
        
        #prompt for answers
        answers = []
        for i in range(4):
            answer = input(f"Enter answer {i+1}: ")
            answers.append(answer)
            
        #prompt for correct answer
        correct_answer = input("Enter the correct answer: ").strip()
        if correct_answer not in answers: 
            print("Invalid input. Correct answer must be one of the provided answers")
            return #this line returns from the function if the correct answer is invalid
        
        #prompt for difficulty level
        difficulty = input("Enter difficulty level (Easy, Medium, Hard): ").capitalize()
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            print("Invalid input. Difficulty level must be 'Easy', 'Medium', or 'Hard'.")
            return
        
        #create the new question object and save it to the database
        new_question = Question(question_text, answers, correct_answer, {"difficulty": difficulty})
        print(f'Your question {new_question} has been successfully added to the database!')
    
    
    