from flask import Flask, request, render_template, redirect
from database import con, cur
import sqlite3
app = Flask(__name__)
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
class User():
    def __innit__(self, email, password, username):
        email = request.form["email"]
        username = request.form['username']
        password = request.form['password'] 

def get_db():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    return con, cur

@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        con, cur = get_db()
        form = RegistrationForm(request.form)
        if request.method == 'POST' and form.validate():
            
            login = request.form['email']
            password = request.form['password']
            
            cur.execute("SELECT email, password FROM user")
            users_db = cur.fetchall()
            for user in users_db:
                if login == user[0] and password == user[1]:
                    con.close()
                    return redirect('/site')
            error = 'Nepareizs lietotājs vai parole'
            con.close() 
            return render_template('login.html', error=error)
        con.close()
        return render_template('login.html', error=error)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    error = ''
    con, cur = get_db()
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            cur.execute("INSERT INTO user (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            con.commit()
            con.close()
            return redirect('/login')
        except Exception as e:
            error = 'Ошибка при добавлении пользователя: ' + str(e)
    con.close()
    return render_template('regestration.html', error=error, form=form)
@app.route("/site")
def site():
    return render_template("site.html")

@app.route("/game")
def game():
    return render_template("game.html")

if __name__ == '__main__':
    app.run(debug=True)