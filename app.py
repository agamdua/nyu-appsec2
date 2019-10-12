import os

import flask

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager

from forms import LoginForm, RegisterForm, SpellCheckForm
from users import User, users, UserDoesNotExist, UniqueConstraintError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'testing')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return users.get_by_id(user_id)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if flask.request.method == 'POST':
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)
            try:
                users.create(user)
            except UniqueConstraintError:
                return render_template(
                    'login_form.html', title='Register', form=form, form_title="Register", registration_failure=True,
                )

            return redirect(url_for('login'))

        else:
            return render_template(
                'login_form.html', title='Register', form=form, form_title="Register", registration_failure=True,
            )

    return render_template(
        'login_form.html', title='Register', form=form, form_title="Register"
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if flask.request.method == 'POST':
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)
            try:
                users.get(user)
            except UserDoesNotExist:
                return render_template(
                    'login_form.html',
                    title='Login',
                    form=form,
                    form_title='Login',
                    login_failure=True,
                )
            return redirect(url_for('spell_check', login_success=True))
        else:
            return render_template(
                'login_form.html',
                title='Login',
                form=form,
                form_title='Login',
                login_failure=True,
            )

    # default is a GET request
    return render_template(
        'login_form.html', title='Login', form=form, form_title="Login"
    )


@app.route('/spell_check')
def spell_check():
    # TODO handle post, right now default get is being used
    login_success = request.args.get('login_success')
    spell_check_form = SpellCheckForm()
    return render_template(
        'spell_check.html', title='Spell Check', form=spell_check_form, form_title="Login", login_success=login_success
    )
