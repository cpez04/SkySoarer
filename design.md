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

"Best Flights": On this page, you can find the "best" flights for you, as determined by the SkyScanner database. Type in the airport IATA code for the origin and destination airport, as well as your departure date, and you will see a chart that details the best flights for you. Results are formatted in JSON and then parsed through specific parameters. We use a dictionary to store the data; the keyse are the operating carrier name, and the values are the price, stop count, flight number, and duration in minutes. We again use try-except to avoid and errors. An apology is thrown if no flights can be found with the user-inputted parameters.

"Flight Tracker": This section only works for flights already in the air! This section also requires two APIs. Once you input the flight IATA number, the flight's latitude and longitude are retrieved via AirLabs. This information is then sent to the HTML site that displays the Google Maps-style with the latitude and longitude of the plane plotted. While we wish we can update the flight's location in real-time, we  unfortunately cannot achieve this due to the limited number of queries we have available. 

"Settings": Here, you can activate/deactivate dark mode as you please. This feature was implemented by making use of the getElementById function to reference the checkbox on the settings page, and adding an event listener that waits for whens the checkbox is clicked or unclicked and toggles the respective body.dark or body.light layer of the CSS. The background and text colors in body.dark and body.light were inverted to ensure readability.



## 2 - Why We Made the Design Choices We Did
The website opts for a clean interface with a sticky navigation bar adapted from Bootstrap. Overall, we use the class .container to create a box with length equals to the viewport length of the user, so that interface always fits the users' screens. At places where we only want to change the font-size, we use .largefont and .medfont. 

"register.html", "login.html": We put the .register_image in <body> to make sure that the background spans through the whole webpage without leaving white spaces at the side. We also set the padding, width, and height in units of vh (viewport height) and vw (viewport width). 

"main_test.html": .welcometext gives the Welcome text a fade-in effect apart from changing the font family and font size. We also implemented a class .reveal to create a reveal effect for the second and third container upon scrolling. We used two tables to contain the pictures and texts, whose width is set using a percentage of the viewport width. There are in total three containers. The class .table sets the default color of the table white. 

"nearby.html", "best.html", "track.html": .page_title sets the top and bottom padding according to viewport height. 