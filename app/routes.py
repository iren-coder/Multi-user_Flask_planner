from datetime import datetime
import functools
from flask import jsonify, render_template, request, redirect, flash, url_for, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user

from app import app, db, login_manager, bcrypt
from .models import Event, User
from .forms import EventForm, LoginForm


@login_manager.user_loader
def user_loader(email):
    return User.query.filter_by(email=email).first()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                session['email'] = form.email.data
                db.session.commit()
                login_user(user, remember=True)
                return redirect('/schedule')
            else:
                return redirect('/login')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/')


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        authenticated = False
        user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'), authenticated=authenticated)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('create_user.html', form=form)


@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    events = db.session.query(Event).order_by(Event.start.desc()).all()
    return render_template('schedule.html', events=events)


@app.route('/add_event', methods=['POST', 'GET'])
@login_required
def event():
    event_form = EventForm()
    if request.method == 'POST':
        if event_form.validate_on_submit():
            author = current_user.email
            start = request.form.get('start')
            end = request.form.get('end')
            subject = request.form.get('subject')
            description = request.form.get('description')
            event = Event(
                author=author, 
                start=start, 
                end=end, 
                subject=subject, 
                description=description)
            db.session.add(event)
            db.session.commit()
            return redirect('/schedule')
        error = 'Ошибка при заполнении формы!'
        return render_template('error.html',form=event_form, error=error)        
    return render_template('add_event.html', form=event_form)


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def event_update(event_id):
    event = db.session.query(Event).filter(Event._id==int(event_id)).first()
    event_form = EventForm(obj=event)
    if request.method == 'POST':
        if event and event_form.validate(): 
            author = current_user.email
            if author != event.author:
                error = 'Редактировать можно только свои события!'
                return render_template('error.html', form=event_form, error=error)
            start = request.form.get('start')
            end = request.form.get('end')
            subject = request.form.get('subject')
            description = request.form.get('description')
            event.author = author
            event.subject = subject
            event.description = description
            event.start = start
            event.end = end
            db.session.commit()
            return redirect('/schedule')
        error = 'Ошибка при заполнении формы!'
        return render_template('error.html',form=event_form, error = error)        
    return render_template('edit_event.html', form=event_form)


@app.route('/event/del/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/schedule')