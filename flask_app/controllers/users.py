from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.home import Home

# MAIN PAGE - REGISTER/LOGIN
@app.route('/')
def index():
    # login/registration page, landing page
    return render_template ('index.html')

# MAIN PAGE - DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        session_user = User.get_user({'id' : session['user_id']})
        all_hosted_homes = Home.get_all_hosted_homes_with_user()
        return render_template ('dashboard.html', session_user=session_user, homes = all_hosted_homes)
    return redirect ('/')

# ACCOUNT PAGE
@app.route('/account')
def account():
    if 'user_id' in session:
        session_user = User.get_user({'id' : session['user_id']})
        return render_template ('account.html', session_user=session_user)
    return redirect ('/')

# UPDATE USER 
# FORM FIELD ---------------------------------------------
@app.route('/update_user', methods=['POST'])
def update_user_form():
    if User.validate_user_update(request.form):
        print(request.form)
        user = User.update_user(request.form)
        return redirect('/account')
    else:
        return redirect('/account')
# --------------------------------------------------------

# =============================================================================================

# REGISTER (LEFT FORM)
@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['register_password'])
    print(pw_hash)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    session['user_id'] = User.create_user(data)
    return redirect ('/dashboard')

# LOGIN (RIGHT FORM)
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# LOGOUT METHOD
@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/') 