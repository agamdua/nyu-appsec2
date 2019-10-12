import os

from flask import Flask, redirect, render_template, url_for

from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'testing')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template(
        './login_form.html', title='Login', form=form
    )


@app.route('/login')
def login():
    form = LoginForm()
    return render_template(
        'login_form.html', title='Login', form=form
    )


@app.route('/spell_check')
def spell_check():
    pass


