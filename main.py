from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, BooleanField, validators
import bcrypt
app = Flask(__name__)



class RegistrationForm(Form):
    def __init__(self, username='', email='', password=''):
        self.username = username
        self.email = email
        self.password = password
    
    def validation_email(self, email):
        if not email.data.endswith("@gmail.com"):
            raise validators.ValidationError('Nepareizs epasts')



    def existis(self, email):
        q = db.session.query(User).filter_by(email=email)
        exist = db.session.query(q.exists()).scalar()
        if exist is True:
            return 0
        else:
            return 1
        
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

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)



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

@app.route("/feedback", methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']

        card = Card(title=title, message=message)
        db.session.add(card)
        db.session.commit()
        return redirect('/site')
    else:
        cards = Card.query.all()
        return render_template("feedback.html", cards=cards)

@app.route("/api/save_score", methods=['POST'])
def save_score():
    try:
        data = request.get_json()
        score = data.get('score', 0)
        user_email = data.get('user_email')  # Пока что используем email для идентификации

        if not user_email:
            return jsonify({'error': 'User email required'}), 400

        # Найти пользователя
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Создать или обновить запись счета
        score_record = Score.query.filter_by(ponal=user.score_shishka).first() if user.score_shishka else None

        if score_record:
            # Обновить существующий счет (если новый счет выше)
            if score > score_record.score_shishka:
                score_record.score_shishka = score
        else:
            # Создать новую запись счета
            score_record = Score(score_shishka=score)
            db.session.add(score_record)
            db.session.flush()  # Получить ID новой записи
            user.score_shishka = score_record.ponal

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Score saved successfully',
            'new_score': score
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/get_score", methods=['GET'])
def get_score():
    try:
        user_email = request.args.get('user_email')
        if not user_email:
            return jsonify({'error': 'User email required'}), 400

        user = User.query.filter_by(email=user_email).first()
        if not user or not user.score_shishka:
            return jsonify({'score': 0})

        score_record = Score.query.filter_by(ponal=user.score_shishka).first()
        score = score_record.score_shishka if score_record else 0

        return jsonify({'score': score})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/leaderboard", methods=['GET'])
def get_leaderboard():
    try:
        # Получить топ 10 игроков с их счетами
        leaderboard = db.session.query(
            User.username,
            User.email,
            Score.score_shishka.label('score')
        ).join(Score, User.score_shishka == Score.ponal)\
         .filter(User.score_shishka.isnot(None))\
         .order_by(Score.score_shishka.desc())\
         .limit(10)\
         .all()

        result = [{
            'username': entry.username,
            'email': entry.email,
            'score': entry.score
        } for entry in leaderboard]

        return jsonify({'leaderboard': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)