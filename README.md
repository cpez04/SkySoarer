Welcome to SkySoarer, a flight tracking website by Herman, Chris, and Ben. Please follow the steps below to navigate this project. There are lots of different files/features to investigate as we go.

We have submitted the website as a zip file skysoarer.zip. Download the file and open the SkySoarer folder on VS code, then execute the following commands in your terminal.

$ cd source
$ ls

Check that the following files are present:

__pycache__             flask_session           nearby.py               templates
app.py                  flight-info.py          prices.py
confirmation.py         flightdistance.py       skysoarer.db
delays.py               helpers.py              static

Now execute:

$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask --app app.py --debug run

This should give the development server on which you can view the website. Ideally, the terminal will output:
 * Running on http://127.0.0.1:5000
INFO: Press CTRL+C to quit

If this is not that case, it may be that the terminal gives you the following error:
ModuleNotFoundError: No module named 'haversine'

This could refer to any preinstalled module that we used, e.g. haversine, emoji, flask etc. In this case execute the following for the required module:

$ pip3 install haversine

Then try running the server again, and once all the modules are installed, open it up on chrome.

You will be prompted to register an account, please do so and then click the Log In tab on the top left of the screen to log in. At this stage you may wish to check you inbox to find a confirmation email from the team!

Hopefully, you have now arrived at a homepage with the message "Welcome, (name)!". Scroll down the see a message from the creators, and even have a look at planes that are in the air above you right now (this is not creepy)! 

You may notice in the footer that for this project we retrieved data from AirLabs, SkyScanner, and Google Maps. We used the following API Key's that you don't have to worry about exporting.

AIRLABS API KEY: c6f24eaf-a7e1-412b-8fdc-f0ca0194c440 
GOOGLE MAPS API KEY: AIzaSyAg3dpTGiCwOvr5QrS0CIuyrET6-lB4fVo

For the airlabs API it is worth noting that we only get 1000 queries on the free plan, so if at any stage you run into a problem with something flight-tracking related on the website, contact us and we will activate another free plan.

Now use the website as you wish. For all the tracking functions, ideally users would know the flight number/IATA code, as this is accessible almost everywhere (boarding passes, phone apps etc.) and they are probably primarily interested in tracking the flights of relatives who have told them their flight number.

Alternatively, you can go to https://www.flightradar24.com/, click on a random flight, get the flight number, and this should be trackable on our website too! That is, of course, with the exception of cargo and private planes etc. that may not be on the database. 

Other functions don't require flight numbers, check out nearby aiports and enter "60" to get all the airports within 60km of your current location. Check out best flights and see what the cheapest flight from "BOS" to "JFK" would be tomorrow!

At some point take a visit to settings to notice we have a dark mode option that allows for a bit of user customization. Turn it on and keep exploring.

Any questions please email:
christopherperez@college.harvard.edu
hleong@college.harvard.edu
bscott@college.harvard.edu

# SkySoarer

AIRLABS API KEY: c6f24eaf-a7e1-412b-8fdc-f0ca0194c440 
GOOGLE MAPS API KEY: AIzaSyAg3dpTGiCwOvr5QrS0CIuyrET6-lB4fVo

Documentation for API (AirLabs): https://airlabs.co/docs/

Note: We only get 1,000 queries for the free plan. 

------------------------------------------------------------------------------------------------------------------------
Steps to running flask project and getting live code changes visible on webpage:
 (refer to: https://stackoverflow.com/questions/16344756/auto-reloading-python-flask-app-upon-code-changes) 
  1. cd into project directory. (native os terminal prefered)
  *you can get path via pwd command*
  2. set environment variables FLASK_APP and FLASK_ENV as outlined in stackoverflow solution (aka):
  
  $ export FLASK_APP=app.py
  
  $ export FLASK_ENV=development
  
  3. When ready to test code, execute the following line in the project directory:
    
    flask --app app.py --debug run

  4. After making code changes. make sure to save the file in your IDE or text editor (ctrl-s).
  
  5. Reload website to view changes.
 
------------------------------------------------------------------------------------------------------------------------
TO PUSH AND PULL CHANGES EASILY:
- DOWNLOAD AND USE GITHUB DESKTOP
------------------------------------------------------------------------------------------------------------------------
Timeline:

11/27 (Sun): simple prototype (webpages and buttons), login and logout functions sessions; CSS; Email/text security confirmation post-registration.

11/30 (Wed): SQL; basic flight tracker; user customization.

12/3 (Sat): Include a map, confirmation email, final touches

12/06 (Tue): PROJECT DEADLINE
  
After each change, execute the following in the terminal:
1. git commit [file name]
2. when the terminal shows "hint: Waiting for your editor to close the file...", type a commit message (i.e. what changes you implemented) in the newly opened window, then close the window.
3. git push

* have to execute git commit for EVERY file that you changed. (until we find an easier way to implement these changes)



