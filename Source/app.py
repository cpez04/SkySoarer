import os
import geocoder
import requests
import json
import geopy
import haversine as hs
import ssl
import smtplib
import random
import emoji

from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from geopy.geocoders import Nominatim
from haversine import Unit
from email.message import EmailMessage

from helpers import apology, login_required


# Configure application hello
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use database
db = SQL("sqlite:///skysoarer.db")

db.execute("CREATE TABLE IF NOT EXISTS userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, hash TEXT NOT NULL, email TEXT NOT NULL)") #userdata table is what we will use to store registered users' info

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
        flight_iata = request.form.get("flight_iata") # used to get flight information based on specific flight IATA number
        
        params = {
        'api_key': 'removed',
        'flight_iata': flight_iata,
        }

        try:
            method = 'flight'
            api_base = 'http://airlabs.co/api/v9/'
            api_result = requests.get(api_base+method, params) # queries Airlabs database
            api_response = api_result.json()['response']
        except:
            return apology("No match", 400) # returns apology if no match found

        # keys store the info we want to show to users
        key = ['dep_name', 'arr_name', 'status', 'dep_time', 'dep_gate', 'arr_gate', 'model'] 
        value = []
        dict = {}

        # retrieve values for each key and appends it to values
        for items in key: 
            try:
                value.append(api_response[items])
            except:
                value.append("Not Available")
            
        key = ['Departure Airport', 'Arrival Airport', 'Flight Status', 'Departure Time', 'Departure Gate', 'Arrival Gate', 'Airplane Model']

        # pair key-value and puts data into the dictionary
        for i in range(len(key)):
            dict[key[i]] = value[i]
            if dict[key[i]] is None:
                dict[key[i]] = 'Not Available'
            else:
                dict[key[i]] = dict[key[i]].title()

        return render_template("searched.html", flight_iata=flight_iata, dict=dict) 
    
    else:
        # used to create the nearby flights at botton of homepage
        params = {
        'api_key': 'removed',
        }
        method = 'flights'
        api_base = 'http://airlabs.co/api/v9/'
        api_result = requests.get(api_base+method, params)
        api_response = api_result.json()["response"]

        latlng=geocoder.ip('me').latlng # retrieves user's latitude and longitude
        latitude = latlng[0]
        longitude = latlng[1]
        usertuple = (latitude,longitude) #formats it into a tuple 

        keys2 = []
        values2 = []
        dict2 = {}

        for row in api_response: # goes through each row in API response to see if the distance from user to plane is < 10 miles
            planetuple = (row['lat'], row['lng'])
            distance = hs.haversine(usertuple, planetuple, unit=Unit.MILES)
            
            if distance < 10: #appends keys based on flights that are <10 miles frm user
                try:
                    keys2.append(row['flight_iata'])
                except:
                    keys2.append("N/A") # makes flight id read N/A if we cannot retrieve flight ID 
                
                values2.append(format(distance, ".2f")) # also adds distance from user 

        numPlanesSky = len(keys2)
        count = 0
        for i in range(numPlanesSky):
            if count == 7: # limits the number of rows in table to 7 flights
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

    # Redirect user to logout page
    return render_template("logout.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("name"): # goes through the following checks to see if user inputted registration info is valid
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
        
        session['name'] = request.form.get("name") # initializes these global variables to acceess them in the email confirmation stage of project
        session['email'] = request.form.get("email")
        session['hash'] = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        
        return redirect("/verification") # redirects to email verification 
        
    
@app.route("/verification", methods=["GET", "POST"])
def verification():
    correct = True
    success = 0 

    if request.method == "GET":
        email_sender = 'skysoarercs50@gmail.com' # sends email to user
        email_password = 'removed'
        email_receiver = session['email']
        session['code'] = random.randint(0,999999) # random code that user must type in, inserted into email 
        
        subject = 'SkySoarer: Account Created'
        body = "Email Verification code: "+ str(session['code']) + "\nSincerely, SkySoarer " + emoji.emojize(':airplane:')

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender,email_receiver, em.as_string())

        return render_template("verification.html", correct=correct)
    
    else:
        while success == 0: # tells user to repeat verification code if they type it in incorrectly 
            if int(request.form.get("verificationcode")) == int(session['code']):
                success = 1 
            else:
                return render_template("verification.html", correct=False)
    
        db.execute("INSERT INTO userdata (name, hash, email) VALUES (?,?,?)", session["name"], session["hash"], session["email"]) # completes registration when code typed in correctly 
        
        return redirect("/login")
        

@app.route("/nearby", methods=["GET", "POST"])
@login_required
def nearby():
    """To get nearby flights"""
    latlng=geocoder.ip('me').latlng # gets user's latitude and longitude
    latitude = latlng[0]
    longitude = latlng[1]
        
    if request.method == "GET":
        geolocator = Nominatim(user_agent="geoapiExercises") # gets info about user's current address, such as city state country zip code 
        location = geolocator.reverse(str(latitude)+","+str(longitude)) 
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        zipcode = address.get('postcode')
        return render_template("nearby.html", city=city, state=state, country=country, zipcode=zipcode)
    else:
        if request.form.get("radius") == "":
            return apology("please type in a number", 400)
        
        radius = float(request.form.get("radius"))*1.609 #converts miles to km
        
        if (radius <= 0):
            return apology("must type positive number", 400)
        
        params = {
        'api_key': 'removed',
        'lat': latitude,
        'lng': longitude,
        'distance': radius
        }
        method = 'nearby'
        api_base = 'http://airlabs.co/api/v9/'
        api_result = requests.get(api_base+method, params)
        api_response = api_result.json()["response"]["airports"] #prints information for airports nearby
        
        keys = []
        values = []
        dicts = {}
        arethereairports = True
        length = len(api_response)
        
        if length == 0: # checks to see if there are nearby airports
            arethereairports = False

        for row in api_response:
            keys.append(row['name'])
            values.append(round(row['distance']/1.609,2)) 
      
        for i in range(length): # creates dictionary where keys are airport name and value is distance converted to miles
            dicts[keys[i]] = values[i] 
           
        return render_template("nearbyed.html", dicts=dicts, arethereairports=arethereairports)
 

@app.route("/settings")
@login_required
def settings():
    """Settings"""
    return render_template("settings.html")

@app.route("/track", methods=["GET","POST"])
@login_required
def track():
    if request.method == "GET":
        return render_template("track.html")
    else:

        # obtain flight_iata from user input
        flight_iata = request.form.get("flight_iata")
        params = {
        'api_key': 'removed',
        'flight_iata': flight_iata,
        }

        # pull out query result, return apology if an error arises
        try:
            method = 'flight'
            api_base = 'http://airlabs.co/api/v9/'
            api_result = requests.get(api_base+method, params)
            api_response = api_result.json()['response']
            latitude = api_response['lat'] # gets flight's latitude and longitude
            longitude = api_response['lng']
        except:
            return apology("No match", 400)

        return render_template("tracked.html", flight_iata=flight_iata, latitude=latitude, longitude=longitude) # returns it to the google map so it can plot flight's location
        

@app.route("/best", methods=["GET", "POST"])
@login_required
def best():
    """Search for best flights"""
    if request.method == "POST":
        url = "https://skyscanner44.p.rapidapi.com/search"

        querystring = {"adults":"1","origin":request.form.get("origin"),"destination":request.form.get("destination"),"departureDate":request.form.get("departureDate"),"currency":"USD"}

        headers = {
            "X-RapidAPI-Key": "removed",
            "X-RapidAPI-Host": "skyscanner44.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        #gets name of operating airlines for 0th row
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

@app.route("/forgotpassword", methods=["GET","POST"])
def forgotpassword():
    if request.method =="GET":
        return render_template("forgotpass.html")
    else:
        if len(db.execute("SELECT email FROM userdata WHERE email = ? LIMIT 1", request.form.get("email"))) == 0:
            return apology("you have not created an account with that username", 400)
        
        session['email'] = request.form.get("email")
        
        return redirect("/passverification")
    
@app.route("/passverification", methods=["GET","POST"])
def passverification():
    correctPass = True
    successPass = 0 
    
    # use email server to send a random code
    if request.method =="GET":
        email_sender = 'skysoarercs50@gmail.com'
        email_password = 'removed'
        email_receiver = session['email']
        session['code'] = random.randint(0,999999)
        
        subject = 'SkySoarer: Password Change Confirmation'
        body = "Password change confirmation code: "+ str(session['code']) + "\nSincerely, SkySoarer " + emoji.emojize(':airplane:')

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender,email_receiver, em.as_string())

        return render_template("passverification.html", correct=correctPass)
    
    else:
        while successPass == 0: 
            if request.form.get("verificationcode") is None:
                return apology("must provide code", 400)
            if int(request.form.get("verificationcode")) == int(session['code']):
                successPass = 1 
            else:
                return render_template("passverification.html", correct=False)

        return redirect("/changepass")
    
@app.route("/changepass", methods=["GET","POST"])
def changepass():
    if request.method == "GET":
        return render_template("changepass.html")
    else:
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Password must be >= 6 characters
        elif len(request.form.get("password")) < 6:
            return apology("password must be > 6 characters")
        elif not request.form.get("confirmpassword"):
            return apology("must provide confirmation", 400)
        elif (request.form.get("password") != request.form.get("confirmpassword")):
            return apology("passwords must match", 400)
        
        db.execute("UPDATE userdata SET hash = ? WHERE email = ?", generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), session['email'])
        
        return redirect("/login")