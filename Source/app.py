import os
import geocoder
import requests
import json

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application hello
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use database
db = SQL("sqlite:///skysoarer.db")

db.execute("CREATE TABLE IF NOT EXISTS userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, hash TEXT NOT NULL, email TEXT NOT NULL)")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    name = db.execute("SELECT name FROM userdata WHERE id = ?", session["user_id"])[0]['name']

    if request.method == "POST":
        flight_iata = request.form.get("flight_iata")
        
        # when user determines a specific flight, returns an info report (maybe here allows save as pdf)
        params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        'flight_iata': flight_iata,
        }

        try:
            method = 'flight'
            api_base = 'http://airlabs.co/api/v9/'
            api_result = requests.get(api_base+method, params)
            api_response = api_result.json()['response']
        except:
            return apology("No match", 400)

        # keys store the info we want to show to users
        key = ['dep_name', 'arr_name', 'status'] 
        value = []
        dict = {}

        # retrieve values for each key
        for items in key:
            value.append(api_response[items])
            
        key = ['Departure Airport', 'Arrival Airport', 'Flight Status']

        # pair key-value
        for i in range(len(key)):
            dict[key[i]] = value[i].title()

        return render_template("searched.html", flight_iata=flight_iata, dict=dict)
    return render_template("main.html", name=name.split()[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM userdata WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("name"):
            return apology("must provide name", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)
        elif len(db.execute("SELECT email FROM userdata WHERE email = ? LIMIT 1", request.form.get("email"))) == 1:
            return apology("you already have an account", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif len(request.form.get("password")) < 6:
            return apology("password must be > 6 characters")
        elif not request.form.get("confirmpassword"):
            return apology("must provide confirmation", 400)
        elif (request.form.get("password") != request.form.get("confirmpassword")):
            return apology("passwords must match", 400)
        
        db.execute("INSERT INTO userdata (name, hash, email) VALUES (?,?,?)", request.form.get("name"), generate_password_hash(
                request.form.get("password"), method='pbkdf2:sha256', salt_length=8), request.form.get("email"))
        
        return render_template("login.html")

@app.route("/nearby", methods=["GET", "POST"])
def nearby():
    """To get nearby flights"""
    if request.method == "GET":
        return render_template("nearby.html")
    else:
        latlng=geocoder.ip('me').latlng
        latitude = latlng[0]
        longitude = latlng[1]
        radius = float(request.form.get("radius"))
        
        if radius <= 0:
            return apology("must type positive number", 400)
        
        params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        'lat': latitude,
        'lng': longitude,
        'distance': radius
        }
        method = 'nearby'
        api_base = 'http://airlabs.co/api/v9/'
        api_result = requests.get(api_base+method, params)
        api_response = api_result.json()["response"]["airports"] #prints informaiton for airports nearby
        
        keys = []
        values = []
        dicts = {}
        arethereairports = True
        length = len(api_response)
        
        if length == 0:
            arethereairports = False

        for row in api_response:
            keys.append(row['name'])
            values.append(row['distance'])
      
        for i in range(length):
            dicts[keys[i]] = values[i]
           
        return render_template("nearbyed.html", dicts=dicts, arethereairports=arethereairports)
 

@app.route("/settings")
def settings():
    """Settings"""
    return render_template("settings.html")

@app.route("/track")
def track():
    return render_template("track.html")

@app.route("/best", methods=["GET", "POST"])
def best():
    """Search for best flights"""
    if request.method == "POST":

       return render_template("bested.html")
    # Redirect user to login form
    return render_template("best.html")
