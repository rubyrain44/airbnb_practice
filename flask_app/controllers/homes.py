from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.home import Home

@app.route('/add_home')
def create_home():
    if 'user_id' in session:
        session_user = User.get_user({'id' : session['user_id']})
        return render_template('add_home.html', session_user=session_user)
    return redirect('/')

# FORM FIELD ---------------------------------------------
@app.route('/host_home', methods=['POST'])
def create_home_form():
    if Home.validate_home(request.form):
        Home.add_home(request.form)
        return redirect('/dashboard')
    else: 
        return redirect('/add_home')
# --------------------------------------------------------

@app.route('/view_home/<int:home_id>')
def view_home(home_id):
    if 'user_id' in session:
        session_user = User.get_user({'id' : session['user_id']})
        data = {
            'id': home_id
        }
        home = Home.get_hosted_home_with_user(data)
        return render_template('view_home.html', session_user=session_user, home=home)
    return redirect('/')

