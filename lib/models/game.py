import sqlite3
import datetime
from models.users import Users

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

#these are the values of what cur_score and then final_score could be 
POINTS = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 25000,
          50000, 100000, 250000, 500000, 1000000]
class Game:

    def __init__(self, user_id, cur_score=0, final_score=0, 
                 date=datetime.datetime.now().date().strftime("%m/%d/%y"), id=None):
        self.cur_score = cur_score
        self.final_score = final_score
        self.date = date
        self.id = id
        self.user_id = user_id
      

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY,
                    cur_score INTEGER,
                    final_score INTEGER,
                    date TEXT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS games;
        """
        CURSOR.execute(sql)
        CONN.commit()
    

    def save(self):

        sql = """
            INSERT INTO games (cur_score, final_score, date, user_id)
            VALUES (?, ?, ?, ?);
        """
        CURSOR.execute(sql, (self.cur_score, self.final_score, self.date, self.user_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        #updates users high score

    @classmethod
    def create(cls, user_id, cur_score=0, final_score=0, 
                 date=datetime.datetime.now().date().strftime("%m/%d/%y"), ):
  
        game = cls(user_id, cur_score, final_score, date)
        game.save()
        return game
    
    @classmethod
    def create_instance(cls, row):
        game = cls(
            final_score=row[2],
            date=row[3],
            user_id=row[4],
            id=row[0] 
        )
        return game 

    @classmethod
    def get_games_by_user(cls, id):
        if(id):
            sql = """ 
                SELECT * FROM games WHERE user_id = ?;
            """
            return [cls.create_instance(row) for row in CURSOR.execute(sql, (id, )).fetchall()]
        else:
            return None 

    def update(self):
        sql = """ 
            UPDATE games SET cur_score = ?, final_score = ?, date = ?, user_id = ? WHERE id = ?;
        """
        CURSOR.execute(sql, (self.cur_score, self.final_score, self.date, self.user_id, self.id))
        CONN.commit()
        
        new_high_score = Users.get_user_high_score(self.user_id)
        if self.final_score > new_high_score:
            Users.update_high_score(self.user_id, self.final_score)

    def update_score(self, index):
        self.cur_score = POINTS[index]
        self.update()


    def __repr__(self):
        return f'\n<Game ID: {self.id}, Final Score: {self.final_score}, Date: {self.date}>'
    

        