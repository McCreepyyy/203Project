from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os


app = Flask(__name__)
app.secret_key = '6969'  # Set a secret key
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
    xp = db.Column(db.Integer, default=0)  # Add this line

    def __repr__(self):
        return '<User %r>' % self.username
    
    def __repr__(self):
        return '<User %r>' % self.username
    


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

@app.route('/lesson5')
def lesson5():
    return render_template('lesson1.html')

@app.route('/lesson6')
def lesson6():
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
    return render_template('quests.html', user=user)

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

