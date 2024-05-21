from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    hearts = db.Column(db.Integer, default=5)
    gems = db.Column(db.Integer, default=0)
    day_streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/characters')
def characters():
    return render_template('characters.html')

@app.route('/leaderboards')
def leaderboards():
    return render_template('leaderboards.html')

@app.route('/quests')
def quests():
    return render_template('quests.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/lessonhubjp')
def lessonhubjp():
    return render_template('lessonhubjp.html')

@app.route('/lessonhubfr')
def lessonhubfr():
    return render_template('lessonhubfr.html')

@app.route('/lessonhub')
def lessonhub():
    # Fetch the user from the database. This is just an example.
    # You'll need to fetch the actual user based on your application's logic.
    user = User.query.first()
    return render_template('lessonhub.html', user=user)

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
        # Update hearts
        hours_since_last_login = (datetime.utcnow() - user.last_login).total_seconds() / 3600
        new_hearts = min(5, user.hearts + int(hours_since_last_login / 4))
        user.hearts = new_hearts

        # Update day streak
        if user.last_login < datetime.utcnow() - timedelta(days=1):
            user.day_streak += 1

        # Update last login
        user.last_login = datetime.utcnow()

        db.session.commit()

        return redirect(url_for('lessonhub'))  # Redirect to lessonhub after login
    else:
        return 'Invalid email or password'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the table again
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)