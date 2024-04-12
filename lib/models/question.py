#lib/models/question.py
from models.__init__ import CURSOR, CONN

class Question:
    
    #dictionary of objects saved to the database
    all = {}
    
    def __init__(self, question, answer1, answer2, answer3, answer4, correct_answer, difficulty, id=None):
        self.id= id
        self.question = question # is this right??? bc question is self
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        
    @classmethod
    def create_table(cls):
        """create a new table to persist the attributes of the question instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer1 TEXT,
                answer2 TEXT,
                answer3 TEXT,
                answer4 TEXT,
                correct_answer TEXT)
                """
        CURSOR.execute(sql)
        CONN.commit()
        
    #drop table classmethod?
    
    
    def display_question(self):
        #displays question and its answer
        print(self.question)
        print("A." + self.answer1)
        print("B." + self.answer2)
        print("C." + self.answer3)
        print("D." + self.answer4)
        
    def check_answer(self, user_answer):
        #check is the user's answer is correct and return the result
        if user_answer.lower() == self.correct_answer.lower():
            return True
        else:
            print("Sorry, that is not the correct answer.")
            return False # but needs more functionality // might be handled in Game class?