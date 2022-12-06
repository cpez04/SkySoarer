Welcome to SkySoarer, a flight tracking website by Herman, Chris, and Ben. Please follow the steps below to navigate this project. There are lots of different files/features to investigate as we go.

1. We have submitted the website as a zip file skysoarer.zip. Before downloading the file, check you have Python 3.11 installed on your computer. Open this folder and double click on the Install certificates.command file to ensure you have the necessary certificates installed and updated so you can operate the website. 

2. Now, download skysoarer.zip and open the SkySoarer folder on VS code. Once this is done, execute the following commands in your terminal:

  $ cd source

  $ cd source 

  $ ls

3. Check that the following files are present:

  __pycache__, app.py, flask_session, helpers.py, skysoarer.db, static, templates

4. Please check to see if you have already installed the extension SQLite Viewer. This will give you access to the skysoarer.db database should you need to open it.

5. Before running flask, also please ensure that you have all necessary libraries already downloaded to your computer. You will see a list of all libraries/modules used in this project at the top of app.py and helpers.py. 

6. Now execute:

  $ flask --app app.py --debug run

This should give the development server on which you can view the website. Ideally, the terminal will output:
 * Running on http://127.0.0.1:5000
INFO: Press CTRL+C to quit

If this is not that case, it may be that the terminal gives you the following error:
ModuleNotFoundError: No module named 'haversine'

This could refer to any preinstalled module that we used, e.g. haversine, emoji, flask etc. In this case execute the following for the required module:

$ pip3 install haversine

Then try running the server again, and once all the modules are installed, open it up on chrome.

7. You will be prompted to register an account. *Register with an email you have access to.* Please do so and then click Register. At this stage you will need to check your inbox to find a verification code from the team (very secure!). After inputting the correct verification code, you will then be prompted to log-in.

8. Hopefully, you have now arrived at a homepage with the message "Welcome, (name)!". Scroll down the see a message from the creators, and scroll further to have a look at planes that are in the air above you right now (this is not creepy)! 

You may notice in the footer that for this project we retrieved data from AirLabs, SkyScanner, and Google Maps. We used the following API Key's that you don't have to worry about exporting. These API keys are already inputted into app.py, so there is no work on your end required to retrieve this data! 

AIRLABS API KEY: c6f24eaf-a7e1-412b-8fdc-f0ca0194c440 
SKYSCANNER API KEY: 49e1e79da8msh462c078111aa514p12ee18jsn10c23c73dcc6
GOOGLE MAPS API KEY: AIzaSyAg3dpTGiCwOvr5QrS0CIuyrET6-lB4fVo

For the AirLabs API, it is worth noting that we only get 1000 queries on the free plan, and for Skyscanner we only get 100. So, if at any stage you run into a problem with something flight-tracking related on the website, contact us and we will activate another free plan. Though prior to submitting we will ensure there are ample queries remaining.

9. Now use the website as you wish. For all the tracking functions, ideally users would know the flight number/IATA code, as this is accessible almost everywhere (boarding passes, phone apps etc.) and they are probably primarily interested in tracking the flights of relatives who have told them their flight number.

Alternatively, you can go to https://www.flightradar24.com/, click on a random flight, get the flight number, and this should be trackable on our website too! That is, of course, with the exception of cargo and private planes etc. that may not be on AirLabs database. 

Other functions don't require flight numbers, check out nearby aiports and enter "60" to get all the airports within 60 miles of your current location. Check out best flights and see what the cheapest flight from "BOS" to "LHR" would be a week from today!

At some point take a visit to settings to notice we have a dark mode option that allows for a bit of user customization. Turn it on and keep exploring.

Should there be any questions or problems, please email:

christopherperez@college.harvard.edu

hleong@college.harvard.edu

bscott@college.harvard.edu
