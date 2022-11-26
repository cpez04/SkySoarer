# SkySoarer

API KEY: c6f24eaf-a7e1-412b-8fdc-f0ca0194c440 

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

11/30 (Wed): SQL; basic flight tracker; user customization

12/3 (Sat): Include a map; print pdf function

12/06 (Tue): PROJECT DEADLINE
  
After each change, execute the following in the terminal:
1. git commit [file name]
2. when the terminal shows "hint: Waiting for your editor to close the file...", type a commit message (i.e. what changes you implemented) in the newly opened window, then close the window.
3. git push

* have to execute git commit for EVERY file that you changed. (until we find an easier way to implement these changes)
