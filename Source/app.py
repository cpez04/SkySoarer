import os
import geocoder
import requests
import json
import geopy
import haversine as hs

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from geopy.geocoders import Nominatim
from haversine import Unit

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
        key = ['dep_name', 'arr_name', 'status', 'dep_time', 'dep_gate', 'arr_gate', 'model'] 
        value = []
        dict = {}

        # retrieve values for each key
        for items in key:
            try:
                value.append(api_response[items])
            except:
                value.append("Not Available")
            
        key = ['Departure Airport', 'Arrival Airport', 'Flight Status', 'Departure Time', 'Departure Gate', 'Arrival Gate', 'Airplane Model']

        # pair key-value
        for i in range(len(key)):
            dict[key[i]] = value[i]
            if dict[key[i]] is None:
                dict[key[i]] = 'Not Available'
            else:
                dict[key[i]] = dict[key[i]].title()

        return render_template("searched.html", flight_iata=flight_iata, dict=dict)
    
    else:
        params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        }
        method = 'flights'
        api_base = 'http://airlabs.co/api/v9/'
        api_result = requests.get(api_base+method, params)
        api_response = api_result.json()["response"]

        latlng=geocoder.ip('me').latlng
        latitude = latlng[0]
        longitude = latlng[1]
        usertuple = (latitude,longitude)  

        keys2 = []
        values2 = []
        dict2 = {}

        for row in api_response:
            planetuple = (row['lat'], row['lng'])
            distance = hs.haversine(usertuple, planetuple, unit=Unit.MILES)
            
            if distance < 10:
                try:
                    keys2.append(row['flight_iata'])
                except:
                    keys2.append("N/A")
                
                values2.append(format(distance, ".2f"))

        numPlanesSky = len(keys2)
        count = 0
        for i in range(numPlanesSky):
            if count == 7:
                break
            dict2[keys2[i]] = values2[i]
            count=count+1
        
        
        return render_template("main_test.html", name=name.split()[0], numPlanesSky=numPlanesSky, dict2=dict2)


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
    latlng=geocoder.ip('me').latlng
    latitude = latlng[0]
    longitude = latlng[1]
        
    if request.method == "GET":
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(latitude)+","+str(longitude))
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        zipcode = address.get('postcode')
        return render_template("nearby.html", city=city, state=state, country=country, zipcode=zipcode)
    else:
        radius = float(request.form.get("radius"))*1.609 #converts miles to km
        
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
            values.append(round(row['distance']/1.609,2))
      
        for i in range(length):
            dicts[keys[i]] = values[i]
           
        return render_template("nearbyed.html", dicts=dicts, arethereairports=arethereairports)
 

@app.route("/settings")
def settings():
    """Settings"""
    return render_template("settings.html")

@app.route("/track", methods=["GET","POST"])
def track():
    if request.method == "GET":
        return render_template("track.html")
    else:
        flight_iata = request.form.get("flight_iata")
        params = {
        'api_key': 'c6f24eaf-a7e1-412b-8fdc-f0ca0194c440',
        'flight_iata': flight_iata,
        }

        try:
            method = 'flight'
            api_base = 'http://airlabs.co/api/v9/'
            api_result = requests.get(api_base+method, params)
            api_response = api_result.json()['response']
            latitude = api_response['lat']
            longitude = api_response['lng']
        except:
            return apology("No match", 400)

        return render_template("tracked.html", flight_iata=flight_iata, latitude=latitude, longitude=longitude)
        

@app.route("/best", methods=["GET", "POST"])
def best():
    """Search for best flights"""
    if request.method == "POST":
        url = "https://skyscanner44.p.rapidapi.com/search"

        querystring = {"adults":"1","origin":request.form.get("origin"),"destination":request.form.get("destination"),"departureDate":request.form.get("departureDate"),"currency":"USD"}

        headers = {
            "X-RapidAPI-Key": "49e1e79da8msh462c078111aa514p12ee18jsn10c23c73dcc6",
            "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

       
        #api_response = response.json()['itineraries']['buckets'][0]['items'][0]['legs'][0]['segments'][0]['operatingCarrier']['name']#gets name of operating airlines for 0th row
        try:
            api_response = response.json()['itineraries']['buckets'][0]['items']
        except:
            return apology("No flights could be found with given parameters", 400)

        keys = []
        values = []
        dict = {}
        length = len(api_response)

        # return apology if no best flight found
        if length == 0:
            return apology("No best flight found", 400)

        # create a list of names
        for i in range(length):
            tmp = []
            keys.append(api_response[i]['legs'][0]['segments'][0]['operatingCarrier']['name']) 

            # insert formatted price, stop count, flight number in tmp
            tmp.append(api_response[i]['price']['formatted'])
            tmp.append(api_response[i]['legs'][0]['stopCount'])
            tmp.append(api_response[i]['legs'][0]['segments'][0]['flightNumber'])
            tmp.append(api_response[i]['legs'][0]['durationInMinutes'])

            # insert tmp into values
            values.append(tmp)

        # set up dict
        for i in range(length):
            dict[keys[i]] = values[i]

        return render_template("bested.html", dict=dict, adults=request.form.get("numAdults"))
    return render_template("best.html")
