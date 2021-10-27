from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
import os
from validate_email import validate_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)
path = "/home/mohamedaziz/files"


mail = Mail(current_app)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
   # if not user or not check_password_hash(user.password, password) or not user.valid:
        #flash('Please check your login details and try again.')
        #return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


s = URLSafeTimedSerializer('thisisasecret!')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user :
        if user.valid==True : 
            flash('Email address already exists')
            return redirect(url_for('auth.signup_post'))
        #elif user.valid==False :
         #   os.rmdir("/home/mohamedaziz/files/"+email)
          #  db.session.delete(user)
           # db.session.commit()
    if 'isi.utm.tn' not in email :
         flash('Please use an isi provided Email')
         return redirect(url_for('auth.signup_post'))
   # is_valid = validate_email(email, verify=True)
    #if not is_valid:
     #   flash('Please use a valid Email address')
      #  return redirect(url_for('auth.signup_post'))
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))
    token = s.dumps(email, salt='email-confirm')
    db.session.add(new_user)
    db.session.commit()
    os.makedirs("/home/mohamedaziz/files/"+email)
    msg = Message(
        'Confirm Email', sender='yesyes02000@gmail.com', recipients=[email])
    link = url_for('auth.confirm_email', token=token,external=True)
    msg.body = 'Your link is {}'.format(link)
    mail.send(msg)
    flash('we sent you a verification mail please check your inbox')
    return redirect(url_for('auth.login'))


@auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        user.valid=True
        db.session.commit()
    except SignatureExpired:
        flash('link expired! Please try making another account')
        return redirect(url_for('auth.signup_post'))
    flash('thank you for confirming your email!')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
