import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Ensure a secret key is set for session management
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'a_very_secret_fallback_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# In-memory user store (replace with a database for a real application)
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_username(username):
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if username == admin_username:
            return User(username)
        return None

# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_username(user_id)

# --- Login Page ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        
        if username == admin_username and password == admin_password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# --- Dashboard ---
@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# --- Logout ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)