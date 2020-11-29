import sqlite3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_user(username, email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
            )
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, email, password FROM users WHERE username = (?)",
                (username,)
                )
    row = cur.fetchone()
    conn.commit()
    conn.close()
    return row

# def get_user(email):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT username, email, password FROM users WHERE email = (?)",
#                 (email,)
#                 )
#     row = cur.fetchone()
#     conn.commit()
#     conn.close()
#     return row

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if get_user(username) is None:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if get_user(username) is None:
        return
    user = User()
    user.id = username
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == get_user(username=username)['password']
    return user

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = get_user(username = username)
        if user:
            if check_password_hash(user['password'], password):

                usr = User()
                usr.id = user['username']
                login_user(usr, remember=form.remember.data)
                return redirect(url_for('dashboard'))
                # return '<h1> You are loggin </h1>'
            return '<h1> Invalid username or password </h1>'
        else:
            return '<h1> Invalid username or password </h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = insert_user(username=form.username.data, email=form.email.data, password=hashed_password)
        return '<h1> New user has been created! </h1>'

    return render_template('signup.html',form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
# @login_required
def logout():
    # logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
