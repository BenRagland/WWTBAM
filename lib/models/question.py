#lib/models/question.py
import sqlite3
CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Question:
    
    #list of objects saved to the database
    all = []
    
    def __init__(self, question="", answers = [], correct_answer="", difficulty="", id=None):
        self.question = question 
        self.answers = answers
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.id = id
        type(self).all.append(self)
        
    @property
    def answers(self):
        return self._answers
    
    @answers.setter
    def answers(self, answers):
        if isinstance (answers, list) and len(answers) == 4:
            self._answers = answers
        else:
            raise Exception("Answers should be a list of 4 answers")
        
            
    @classmethod
    def create_table(cls):
        """create a new table to persist the attributes of the question instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answers BLOB,
                correct_answer TEXT,
                diifficulty TEXT)
                """
        CURSOR.execute(sql)
        CONN.commit()
        
    #drop table classmethod? #BUILD THIS TODAY SATURDAY
    
    
    # def display_question(self):
    #     #displays question and its answer
    #     print(self.question)
    #     print("A." + self.answer1)
    #     print("B." + self.answer2)
    #     print("C." + self.answer3)
    #     print("D." + self.answer4)
        
    # def check_answer(self, user_answer):
    #     #check is the user's answer is correct and return the result
    #     if user_answer.lower() == self.correct_answer.lower():
    #         return True
    #     else:
    #         print("Sorry, that is not the correct answer.")
    #         return False # but needs more functionality // might be handled in Game class?
        
    
    
    