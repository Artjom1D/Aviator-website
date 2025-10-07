from flask import Flask, request, render_template, redirect
from database import con, cur
import sqlite3
app = Flask(__name__)

def get_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    return con, cur

@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        con, cur = get_db()
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            cur.execute("SELECT email, password FROM user")
            users_db = cur.fetchall()
            for user in users_db:
                if form_login == user[0] and form_password == user[1]:
                    con.close()
                    return redirect('/site')
            error = 'Nepareizs lietotājs vai parole'
            con.close()
            return render_template('login.html', error=error)
        con.close()
        return render_template('login.html', error=error)

@app.route('/reg' , methods=['GET', 'POST'])
def reg():
        error = ''
        con, cur = get_db()
        if request.method == 'POST':
            form__email = request.form['email']
            form__password = request.form['password']
            form__username = request.form['username']
            cur.execute("INSERT INTO user (email, password, username) values (?, ?, ?)", (form__email, form__password, form__username))
            con.commit()
            con.close()
            return render_template('login.html', error=error)
        
        else:
            con.close()
            return render_template('regestration.html', error=error)
@app.route("/site")
def site():
    return render_template("site.html")

@app.route("/game")
def game():
    return render_template("game.html")

if __name__ == '__main__':
    app.run(debug=True)