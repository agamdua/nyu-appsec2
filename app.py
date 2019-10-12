import os

from flask import Flask, render_template

from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'testing')

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


