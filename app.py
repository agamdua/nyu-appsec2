import os

import flask

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    UserMixin,
)
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegisterForm, SpellCheckForm
from utils import run_spell_check

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "testing")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# TODO: remove or restrict to tests!
# app.config["WTF_CSRF_ENABLED"] = False

db = SQLAlchemy(app)

from models import User, SpellCheck, Roles

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db.create_all()
test_user = User(username="test", password="test")
test_user.save()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)

            # TODO: add additional verfication checks
            if user.username == 'admin':
                user.role = Roles.admin
            try:
                user.save()
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
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                return render_template(
                    "login_form.html",
                    title="Login",
                    form=form,
                    form_title="Login",
                    login_failure=True,
                )
            user.create_session()
            user.save()
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
            out = run_spell_check(input_data)

            spell_check = SpellCheck(
                text_to_check=input_data, result=out, user=current_user
            )
            spell_check.save()
            return redirect("spell_check")

    if flask.request.method == "GET":
        spell_check = SpellCheck.query.filter_by(user_id=current_user.id).first()
        input_data = getattr(spell_check, "text_to_check", None)

        login_success = request.args.get("login_success")
        return render_template(
            "spell_check.html",
            title="Spell Check",
            form=spell_check_form,
            input_data=input_data,
            login_success=True,
        )


@app.route("/history")
@app.route("/history/query<qid>")
@login_required
def history(qid=None):
    spell_check_queries = SpellCheck.query.filter_by(user_id=current_user.id).all()

    # given that we don't have enough that requires pagination, calculated the count in python shouldn't be too big a deal
    count = len(spell_check_queries)

    # TODO
    """
    if current_user.role == 'admin':
        don't filter by user
    else definitely add the user filter on the query
    """

    if qid is not None:
        query = SpellCheck.query.filter_by(id=qid)
        if current_user.role != Roles.admin:
            query = query.filter_by(user_id=current_user.id)
    else:
        query = None

    return render_template(
        "spell_check_history.html",
        queries=spell_check_queries,
        count=count,
        qid=qid,
        user=current_user,
        query=query,
    )
