import os
import subprocess

import flask

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, LoginManager, login_required, login_user
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegisterForm, SpellCheckForm
from users import User, users, UserDoesNotExist, UniqueConstraintError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "testing")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# TODO: remove or restrict to tests!
app.config["WTF_CSRF_ENABLED"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class UserTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_authenticated = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)


@login_manager.user_loader
def load_user(user_id):
    return users.get_by_id(user_id)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)
            try:
                users.create(user)
            except UniqueConstraintError:
                return render_template(
                    "login_form.html",
                    title="Register",
                    form=form,
                    form_title="Register",
                    registration_failure=True,
                )

            return render_template(
                "login_form.html",
                title="Register",
                form=form,
                form_title="Register",
                registration_success=True,
            )

        else:
            return render_template(
                "login_form.html",
                title="Register",
                form=form,
                form_title="Register",
                registration_failure=True,
            )

    return render_template(
        "login_form.html", title="Register", form=form, form_title="Register"
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)
            try:
                users.get(user)
            except UserDoesNotExist:
                return render_template(
                    "login_form.html",
                    title="Login",
                    form=form,
                    form_title="Login",
                    login_failure=True,
                )
            user.create_session()
            users._save(user)
            login_user(user)
            return redirect(url_for("spell_check"))
        else:
            return render_template(
                "login_form.html",
                title="Login",
                form=form,
                form_title="Login",
                login_failure=True,
            )

    # default is a GET request
    return render_template(
        "login_form.html", title="Login", form=form, form_title="Login"
    )


@app.route("/spell_check", methods=["GET", "POST"])
@login_required
def spell_check():
    spell_check_form = SpellCheckForm()

    if flask.request.method == "POST":
        if spell_check_form.validate_on_submit():
            input_data = spell_check_form.inputarea.data
            out = subprocess.run(["./a.out", input_data], stdout=subprocess.PIPE)
            current_user.input_data = input_data
            current_user.out = out
            return redirect("spell_check")

    if flask.request.method == "GET":
        input_data = getattr(current_user, "input_data", None)
        login_success = request.args.get("login_success")
        return render_template(
            "spell_check.html",
            title="Spell Check",
            form=spell_check_form,
            input_data=input_data,
            login_success=True,
        )
