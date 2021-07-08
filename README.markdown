<h1>AVAILABILITY CHECKER</h1>

<p>Automatically checks for appointment for passport renewals at the Italian Consulate in London, UK. It works for the current month and the next two.</p>
<br>
<h2>MOTIVATION</h2>
<p>Getting appointments for passport renewals at the Italian Consulate in London is infamously difficult, with gangs illegally selling appointments at a premium price.</p>
<p>This code regularly checks for availability and alerts users, via SMS and email, as soon as a slot becomes available.</p>
<p>I was able to book an appointment two days after implementing this code.</p>
<p>Frankly, the Italian Consulate should offer this notification service themselves...</p>
<br>
<h2>COMPATIBILITY</h2>
<p>MacOS with Chrome</p>
<br>
<h2>SETUP</h2>

1. On Mac, open Terminal ('CMD + spacebar' and type Terminal), create a folder to hold the project files and access the directory:

   ```
   mkdir italian_consulate && cd italian_consulate
   ```
2. Create a virtual environment for the app to run. I chose to name mine '.italian_consulate'. The dot in front of the name makes the virtual environment isolated from the rest of the system (also makes it invisible):

   ```
   python3 -m venv .italian_consulate
   ```
3. Activate the virtual environment:

   ```
   . .italian_consulate/bin/activate 
   ```
4. Install the dependencies from 'requirements.txt' using pip:

   ```
   pip install -r requirements.txt
   ```
5. Open a free trial account with Twilio by following the steps described here: https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account
   &nbsp;
6. This app will need to control Chrome to interact with the Italian Consulate's webpage. In order for it to do so, you'll also need to download a driver for Chrome. Download the driver for your veresion of Chrome here: https://sites.google.com/a/chromium.org/chromedriver/downloads

   Save the driver to the following folder: '/usr/local/bin/'
   &nbsp;
7. Once logged into your Twilio account, navigate to your console (https://www.twilio.com/console) and select 'Dashboard'.
   &nbsp;
8. Under 'Project Info', take note of
   a) your ACCOUNT SID and
   b) AUTH TOKEN.
   &nbsp;
9. You'll also need to take note of c) your TWILIO PHONE NUMBER, which can be found by clicking on the three dots on the left of your console page, under the home tab. This number is where the SMS will be sent from. You will also need to have d) your own MOBILE NUMBER.
   &nbsp;
10. Once you have Twilio's ACCOUNT SID, AUTH TOKEN, TWILIO PHONE NUMBER and MOBILE NUMBER, in your Terminal window export them as environment variables as follows:

    ```
    export ACC_SID='your_account_sid'
    export AUTH_TOKEN='your_auth_token'
    export TWILIO_NUM='your_twilio_phone_number'
    export MOB_NUM='your_mobile_number'
    ```

    &nbsp;
11. Now you'll need to export your login details as environment variables. These are saved to be used each time you get logged out (which happens automatically each couple of hours).

************************************************************************************************* IT'S STRONGLY RECOMMENDED THAT YOU CREATE A UNIQUE LOG IN FOR THIS WEBSITE! I AM NOT RESPONSIBLE FOR ANYTHING THAT GOES WRONG WITH YOUR CREDENTIALS, OR IN CASE OF DATA LEAKS! NOTHING IS HASHED HERE, AND I GAVE VERY LITTLE CONSIDERATION TO SECURITY IN THIS CODE! *************************************************************************************************

```
export EMAIL="your_email_goes_here"
export PW="your_password_goes_here"
```

&nbsp;

<h2>RUNNING THE CODE</h2>
1. In Terminal, with the virtual environment still active (see step 3, above), run the code as follows:

```
python main.py 
```

2. You don't need to do anything else: the app will automatically check for available appointments in the current month and the following two months. It does this every 25 seconds.

If a free slot is found, a voice message will be played in your computer, and you'll receive an SMS. You will then have to login and manually complete the booking directly on the consulate's website.
&nbsp;

<br>
<h2>LICENSE</h2>
<p><a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU GPLv3</a></p>
