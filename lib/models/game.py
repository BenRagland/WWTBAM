import sqlite3
import datetime

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

POINTS = ['$100', '$200', "$300", "$500", "$1,000", "$2,000", "$4,000", "$8,000", "$16,000", "$25,000",
          "$50,000", "$100,000", "$250,000", "$500,000", "$1,000,000"]
class Game:

    def __init__(self, cur_score='$0', final_score='$0', 
                 date=datetime.datetime.now().date().strftime("%m/%d/%y"), id=None, user_id=None):
        self.cur_score = cur_score
        self.final_score = final_score
        self.date = date
        self.id = id
        self.user_id = user_id
        self.save()

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games
                (
                    id INTEGER PRIMARY KEY,
                    cur_score TEXT,
                    final_score TEXT,
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
  
    @classmethod
    def create(cls, cur_score, final_score, date, user_id):
        game = cls(cur_score, final_score, date, user_id)
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

    def update_score(self, index):
        self.cur_score = POINTS[index]
        self.update()

    def __repl__(self):
        return f'<Game ID: {self.id}, High Score: {self.final_score}, Date: {self.date}'