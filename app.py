from flask import Flask, request, render_template, redirect, url_for
import sqlite3, sys
from database_setup import init_db

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def test_fnctn():
    if request.method == "POST":
        user_name = request.form["name"]
        user_email = request.form["email"]
        user_message = request.form["message"]
        if not user_name or not user_email or not user_message:
            return "Bad Request: Name, email and message are required!", 400
        elif len(user_message) > 500:
            return "Bad Request: Too many characters!", 400
        else:
            con = get_db()
            cur = con.cursor()
            sql = "INSERT INTO entries (name, email, message) VALUES (?, ?, ?)"
            cur.execute(sql, (user_name, user_email, user_message))
            con.commit()
            db_close(con)
            return redirect(url_for("test_fnctn"))
    if request.method == "GET":
        con = get_db()
        cur = con.cursor()
        res = cur.execute("SELECT * FROM entries ORDER BY created_at DESC")
        data = res.fetchall()
        db_close(con)
        return render_template("index.html", entries=data)
    
@app.route("/delete/<id_num>", methods=["GET"])
def del_entry(id_num):
    con = get_db()
    cur = con.cursor()
    print(id_num, (type(id_num)))
    cur.execute("DELETE FROM entries WHERE id = ?", (id_num,))
    con.commit()
    db_close(con)
    return redirect(url_for("test_fnctn"))
    
def get_db():
    try:
        con = sqlite3.connect("guestbook.db")
        con.row_factory = sqlite3.Row
        return con
    except sqlite3.OperationalError as e:
        print("Operational Error connecting to user database: ", e)
        sys.exit(e)

def db_close(con):
    if con is not None:
        con.close()