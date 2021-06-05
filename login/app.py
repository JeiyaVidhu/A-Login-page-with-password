from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
from db_functions import get_password, insert_user

app = Flask(__name__)
app.secret_key = "123@abc"
app.permanent_session_lifetime = timedelta(minutes=5)

def set_session(email):
    session.permanent = True
    session["logged_in"] = True
    session["email"] = email


def reset_session():
    if "logged_in" in session:
        del session["logged_in"]
        del session["email"]


def verify_login(email, password):
    stored_password = get_password(email)
    if len(stored_password):
        if password == stored_password[0][0]:
            set_session(email)
            return redirect("/")
        else:
            print("wrong password")
            return redirect("/")
    else:
        insert_user(email, password)
        set_session(email)
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        verify_login(email, password)
        return redirect(url_for('index'))

@app.route("/logout")
def logout():
    reset_session()
    return redirect("/")

@app.route("/")
def index():
    if "logged_in" in session:
        return render_template('welcome.html', email=session["email"])
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)