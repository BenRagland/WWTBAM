import sqlite3
import datetime

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Users:
    def __init__(self,name,high_score = 0,id="none"):
        self.id = id
        self.name = name
        self.high_score = high_score

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,name):
        if not (isinstance(name,str)):
            raise TypeError("name must be a string")
        else:
            self._name = name.upper()

    
    #validate name Method
    def __repr__(self):
        return(f'<{self.id} Owner "{self.name}" {self.high_score} />')
    
    @classmethod
    def create_table(cls):
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY
                name TEXT
                high_score INTEGER
            )
            """
        CURSOR.execute(sql)
        CONN.commit()
    
   
    def save(self):
        try:
            sql= """
                INSERT INTO Users (name) VALUES (?);
                """
            CURSOR.execute(sql,(self.name))
            # set ID
            self.id = CURSOR.lastrowid
            CONN.commit()
        except Exception as err:
            Exception (f'Save went wrong,${err}')

    @classmethod
    def create_row(cls,name):
        user = cls(name)
        user.save()
        return user
    
    @classmethod
    def delete_row(cls,id):
        try:
            sql = """ 
                DELETE FROM users WHERE id = ?;
            """
            CONN.execute(sql, (id))
            CONN.commit()
            print("success")
        except Exception as err:
            print(f'error:{err}')

    #Create Instance from Row
    @classmethod
    def create_instance(cls,row):
        user = cls(
            id = row[0],
            name = row [1],
            high_score = row[2]
        )
        return user
    
    def update(self):
        try:
            sql="""
                    UPDATE users SET name = ?, high_score = ?, where id = ?
                """
            CURSOR.execute(sql,(self.name, self.high_score,self.id))
            CONN.commit()
            print(f"successfully saved ${self.name}")
        except Exception as err:
            print (f"Error Updating ${self.name}: ${err}" )


    @classmethod 
    def find_by_id(cls, id):
        sql = """
                SELECT * FROM users WHERE id=?;
            """
        row = CURSOR.execute(sql,(id)).fetchone()
        if not row: 
            return None 
        else: 
            return cls.create_instance(row)
    
    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS users;"""
        CURSOR.execute(sql)
        CONN.commit()