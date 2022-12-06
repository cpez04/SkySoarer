## 1 - How We Implemented Our Project:
SkySoarer was implemented using HTML, Python, CSS, and SQL. 

Problem set 9 (Finance) provided a very basic framework for how we implemented our website; however, we expanded upon our knowledge of coding languages and added many creative liberties to create a seamless user experience.

Upon entering our website (run with Flask), you are directed to our register page. Here, you must input a First and Last Name, a valid email, and a 6 character (or greater) in length password that must also be confirmed below. If any one of the fields are incorrect or invalid, an apology will appear - you must try registering again! 

Upon clicking "Register," the library smtplib and email.message are utilized to send an Account Created email to the email specified in the registration form, using the GMAIL email server. In this email you will find a random 6-digit verification code that the user must correctly type in to finalize registration. Once typed in, the userdata table is updated to reflect the addition of a new user to SkySoarer. His or her name, hashed password (using generate_password_hash from wekzeug.security), and email are stored in this table. 

Now the user can log in. Log in credentials are checked within the userdata table to ensure the user exists. If not, an apology will appear. 

Inside the welcome page, you are greeted with "Welcome, {{name}}" to add a touch of personalization. We did this by splitting the user's full name to retrieve the first name and sending this variable over to the main_test.html and displaying it using Jinga. 

Scroll down for more information about our creators. Further down, we have a section titled "Look above!" The below table shows a selection of flights within 10 miles of you. Your latitude and longitude is determined using the geopy library, and then we query the AirLabs database to get each flight's latitude and longitude. Distance between yourself and the plane is calculated using the haversine library, and if distance < 10 (miles), the result is added to the table. We limited the size of the table to show up to 7 flights for space's sake. 

Back at the top of the homepage, you type in a flight IATA code to get basic information about the flight of your choice. If you had access to a boarding pass, you'd already know this ID. However, if you don't have a flight IATA code to look up, you can easily choose a flight from https://www.flightradar24.com/34.4,-83.61/11, although please note not all flights may be reflected in the AirLabs database. Best to choose a commercial airline. Entering the code queries the AirLabs database to retrieve departure airport, arrival flight, flight status, departure time, departure gate, arrival gate, and airplane model. If any of these fields were unavailable in the database, an error would be thrown. To avoid this, we use try-except to just return "Not Available" for the corresponding row. 

"Nearby Airports": Upon loading this page, it prints out information about where you currently are by using your latitude and longitude as previously determined. Type in a search radius in miles, and the AirLabs database is queried to find the airports within X miles of you. Results are printed in a similar table to that of Finance.

"Best Flights": 





## 2 - Why We Made the Design Choices We Did
