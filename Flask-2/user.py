import sqlite3
from flask_restful import Resource
from flask import request

class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password
    
    @classmethod
    def find_by_username(cls,username):
        conn=sqlite3.connect('data.db')
        cursor=conn.cursor()

        q1 = "SELECT * FROM user WHERE username=?"
        result=cursor.execute((q1,username,))
        row=result.fetchone()
        if row:
            user=cls(*row)
        else:
            user=None
        return user
    @classmethod
    def find_by_id(cls,id):
        conn=sqlite3.connect('data.db')
        cursor=conn.cursor()

        q1 = "SELECT * FROM user WHERE username=?"
        result=cursor.execute(q1,(id,))
        row=result.fetchone()
        if row:
            user=cls(*row)
        else:
            user=None
        return user

    

class signup(Resource):
    def post(self):
        data=request.get_json()
        username = data['username']
        password = data['password']

        conn=sqlite3.connect('data.db')
        cursor=conn.cursor()

        q1 = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY,username TEXT,password TEXT)"
        cursor.execute(q1)
        q2 = "INSERT INTO user VALUES (NULL, ?, ?)"
        cursor.execute(q2, (username, password))

        conn.commit()
        conn.close()
        return {"message":"user created"}