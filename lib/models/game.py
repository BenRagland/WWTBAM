import sqlite3
import datetime

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()


class Game:

    all_games = {}

    def __init__(self, cur_score=0, final_score=0, date=datetime.datetime.now().date(), id=None, user_id=None):
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
    