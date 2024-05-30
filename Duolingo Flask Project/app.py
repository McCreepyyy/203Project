# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os


app = Flask(__name__)
app.secret_key = '6969'  # Set a secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
db = SQLAlchemy(app)

app = Flask(__name__)
app.secret_key = '6969'  # Set a secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
db = SQLAlchemy(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    hearts = db.Column(db.Integer, default=5)
    gems = db.Column(db.Integer, default=0)
    day_streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    xp = db.Column(db.Integer, default=0)  # Add this line

    def __repr__(self):
        return '<User %r>' % self.username

class DailyQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    reward = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_assigned = db.Column(db.Date, default=date.today)

    user = db.relationship('User', backref=db.backref('quests', lazy=True))

def generate_daily_quests(user):
    today = date.today()
    if DailyQuest.query.filter_by(user_id=user.id, date_assigned=today).count() > 0:
        return

    quests_descriptions = [
        "Earn 100 XP",
        "Buy an item from the shop",
        "Complete a lesson",
        "Win a game",
        "Log in two times today"
    ]

    for _ in range(3):
        description = random.choice(quests_descriptions)
        reward = random.randint(10, 50) // 10 * 10  # Ensure reward is a multiple of 10
        quest = DailyQuest(user_id=user.id, description=description, reward=reward, date_assigned=today)
        db.session.add(quest)
    db.session.commit()




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lesson1')
def lesson1():
    return render_template('lesson1.html')


@app.route('/lesson2')
def lesson2():
    return render_template('lesson1.html')

@app.route('/lesson3')
def lesson3():
    return render_template('lesson1.html')

@app.route('/lesson4')
def lesson4():
    return render_template('lesson1.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/getstarted')
def getstarted():
    return render_template('getstarted.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/indexjp')
def indexjp():
    return render_template('indexjp.html')

@app.route('/indexfr')
def indexfr():
    return render_template('indexfr.html')

@app.route('/lessonhub')
def lessonhub():
    user = User.query.get(session['user_id'])  # Get the current user
    top_users = User.query.order_by(User.xp.desc()).limit(3).all()  # Get top 3 users
    return render_template('lessonhub.html', user=user, top_users=top_users)

@app.route('/katakana')
def katakana():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('katakana.html', user=user)

@app.route('/characters')
def characters():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('characters.html', user=user)

@app.route('/leaderboards')
def leaderboards():
    # Fetch all users and sort them by XP in descending order
    all_users = User.query.order_by(User.xp.desc()).limit(10).all()
    return render_template('leaderboards.html', users=all_users)

@app.route('/quests')
def quests():
    user = User.query.get(session['user_id'])  # Get the current user
    generate_daily_quests(user)  # Ensure the user has quests for today
    quests = DailyQuest.query.filter_by(user_id=user.id, date_assigned=date.today()).all()
    return render_template('quests.html', user=user, quests=quests)


@app.route('/complete-quest/<int:quest_id>', methods=['POST'])
def complete_quest(quest_id):
    quest = DailyQuest.query.get(quest_id)
    if quest and quest.user_id == session['user_id'] and not quest.completed:
        quest.completed = True
        user = User.query.get(session['user_id'])
        user.gems += quest.reward
        db.session.commit()
    return redirect(url_for('quests'))


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    user = User.query.get(session['user_id'])  # Get the current user
    if request.method == 'POST':
        # Check which item is being purchased
        item_id = request.form['item_id']
        if item_id == 'hearts':
            if user.gems >= 350:
                user.gems -= 350
                user.hearts = 5
                db.session.commit()
            # Whether sufficient or not, redirect back to the shop page
            return redirect(url_for('shop'))
        elif item_id == 'streak_freeze':
            if user.gems >= 200:
                user.gems -= 200
                # Logic for streak freeze
                db.session.commit()
            # Whether sufficient or not, redirect back to the shop page
            return redirect(url_for('shop'))
        else:
            return 'Invalid item ID.'

    # Render the shop page with available items
    return render_template('shop.html', user=user)  # Pass the User object to the template

@app.route('/settings')
def settings():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('settings.html', user=user)

@app.route('/profile')
def profile():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('profile.html', user=user)

@app.route('/lessonhubjp')
def lessonhubjp():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('lessonhubjp.html', user=user)

@app.route('/lessonhubfr')
def lessonhubfr():
    user = User.query.get(session['user_id'])  # Get the current user
    return render_template('lessonhubfr.html', user=user)



@app.route('/submit_form', methods=['POST'])
def submit_form():
    print("Form data: ", request.form)
    age = request.form['age']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user = User(username=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('signin'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        hours_since_last_login = (datetime.utcnow() - user.last_login).total_seconds() / 3600
        if hours_since_last_login >= 6:
            user.hearts = 5  # Reset hearts every 6 hours
        else:
            new_hearts = min(5, user.hearts + int(hours_since_last_login / 4))
            user.hearts = new_hearts
        if user.last_login < datetime.utcnow() - timedelta(days=2):  # Check if 48 hours have passed
            user.day_streak = 0  # Reset streak if 48 hours have passed
        elif user.last_login < datetime.utcnow() - timedelta(days=1):
            user.day_streak += 1  # Increment streak if 24 hours have passed
        user.last_login = datetime.utcnow()
        db.session.commit()
        session['user_id'] = user.id  # Set the user id in the session
        return redirect(url_for('lessonhub'))  
    else:
        return 'Invalid email or password'   

@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    data = request.json
    user = User.query.get(session['user_id'])  # Get the current logged-in user
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if data.get('password'):
        user.password = data['password']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/toggle_dark_mode', methods=['POST'])
def toggle_dark_mode():
    data = request.json
    dark_mode = data.get('darkMode', False)
    # Here you would save the dark mode preference to the user profile or session
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

