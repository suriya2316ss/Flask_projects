from flask import Flask,request,jsonify
import sqlite3,os

DB="todo.db"
def init_db():
    conn=sqlite3.connect(DB)
    c=conn.cursor()
    query1="CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, title TEXT, done INTEGER)"
    c.execute(query1)
    conn.commit()
    conn.close()

def query(sql,args=(),one=False):
    conn=sqlite3.connect(DB)
    curr=conn.execute(sql,args)
    rv=[]
    rows=curr.fetchall()
    for row in rows:
        task={
        "id":row[0],
        "title":row[1],
        "done":bool(row[2])
        }
    rv.append(task)

app=Flask(__name__)
init_db()

@app.route("/tasks",methods=["GET","POST"])
def tasks():
    if request.method=="GET":
        return jsonify(query("SELECT * FROM tasks"))
    data=request.get_json() or {}
    title=data.get("title","Untitled")
    conn=sqlite3.connect(DB)
    curr=conn.cursor()
    curr.execute("INSERT INTO tasks(title,done)VALUES(?,?)",(title,0))
    conn.commit()
    nid=curr.lastrowid
    conn.close()
    return jsonify({"id":nid,"title":title,"done":False}),201

@app.route("/tasks/<int:tid>",methods=["GET","PUT","DELETE"])
def task(tid):
    if request.method=="GET":
        t=query("SELECT * FROM tasks WHERE id=?",(tid,),one=True)
        return jsonify(t or {}),(200 if t else 404)
    if request.method=="PUT":
        data=request.json or {}
        title=data.get("title")
        done = 1 if data.get("done") else 0
        conn=sqlite3.connect(DB)
        curr=conn.cursor()
        curr.execute("UPDATE tasks SET title=?,done=? WHERE id=?",(title,done,tid))
        conn.commit()
        conn.close()
        return jsonify({"id":tid,"title":title,"done":bool(done)})
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?",(tid,))
    conn.commit()
    conn.close()
    return "",204

if __name__=="__main__":
    app.run(debug=True)


        
    