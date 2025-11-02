from flask import Flask, request, render_template, redirect
import sqlite3
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, BooleanField, validators
import bcrypt
app = Flask(__name__)





app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def hashed_str(plain_text):
    return bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_str(plain_text, hashed_str):
    if isinstance(hashed_str, str):
        hashed_str = hashed_str.encode('utf-8')
    return bcrypt.checkpw(plain_text.encode('utf-8'), hashed_str)
db = SQLAlchemy(app)
class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    score_shishka = db.Column(db.Integer, db.ForeignKey('score.ponal'))


class Score(db.Model):
    ponal = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score_shishka = db.Column(db.Integer, nullable=False)




class RegistrationForm(Form):
    def __init__(self, username='', email='', password=''):
        self.username = username
        self.email = email
        self.password = password
    
    def validation_email(self, email):
        if not email.data.endswith("@gmail.com"):
            raise validators.ValidationError('Nepareizs epasts')






@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        form = RegistrationForm(request.form)
        if request.method == 'POST':
            form.email = request.form['email']
            if not form.email.endswith("@gmail.com") and form.validation_email(form.email):
                error = 'Nepareizs epasts'
                return render_template('login.html', error=error)
            form.password = request.form['password']
            users_db = User.query.all()
            for user in users_db:
                
                if form.email == user.email and check_str(form.password, user.password):
                    return render_template('site.html', error=error)
            else:
                error = 'Nepareizs lietotājs vai parole'
                return render_template('login.html', error=error)

            
        else:
            return render_template('login.html', error=error)

@app.route('/reg' , methods=['GET', 'POST'])
def reg():
        error = ''
        form = RegistrationForm(request.form)
        if request.method == 'POST':
            form.username = request.form['username']
            form.email = request.form['email']
            if not form.email.endswith("@gmail.com") and form.validation_email(form.email):
                error = 'Nepareizs epasts'
                return render_template('regestration.html', error=error)
            form.password = request.form['password']
        
            hashed_password = hashed_str(form.password)
            user = User(email=form.email, password=hashed_password, username=form.username)
            db.session.add(user)
            db.session.commit()
        
            return render_template('login.html', error=error)
        else:    
            return render_template('regestration.html', error=error)
@app.route("/site")
def site():
    return render_template("site.html")

@app.route("/game")
def game():
    return render_template("game.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)