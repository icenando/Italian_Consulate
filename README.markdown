<h1>AVAILABILITY CHECKER</h1>
<p>Automatically checks for appointment slots at the Italian Consulate in London, UK.</p>
<br>
<h2>MOTIVATION</h2>
<p>Getting appointments for passport renewals at the Italian Consulate in London is infamously difficult, with gangs illegally selling appointments at a premium price. This code regularly checks for availability and alerts users, via SMS and email, as soon as a slot becomes available.</p>
<p>I was able to book an appointment two days after implementing this code. It could be easily adapted for other online booking systems.</p>
<br>
<h2>SETUP</h2>

1. On Mac, open Terminal ('CMD + spacebar' and type Terminal), create a folder to hold the project files and access the directory:

   ```
   mkdir italian_consulate && cd italian_consulate
   ```
2. Create a virtual environment for the app to run. I chose to name mine '.italian_consulate'. The dot in front of the name makes the virtual environment isolated from the rest of the system (also makes it an invisible):

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
6. This app will need to control a browser window to interact with the Italian Consulate's webpage. In order for it to do so, you'll also need to download a driver for Chrome. Download the driver for your veresion of Chrome here: https://sites.google.com/a/chromium.org/chromedriver/downloads

   Save the driver to the following folder: '/usr/local/bin/'
   &nbsp;
7. Once logged into your Twilio account, navigate to your console (https://www.twilio.com/console) and select 'Dashboard'.
   &nbsp;
8. Under 'Project Info', take note of
   a) your ACCOUNT SID and
   b) AUTH TOKEN.
   &nbsp;
9. You'll also need to take note of c) your TWILIO PHONE NUMBER, which can be found by clicking on the three dots on the left of your console page, under the home tab. This number is where the SMS will be sent from. You will also need to have your own MOBILE NUMBER.
   &nbsp;
10. Once you have Twilio's ACCOUNT SID, AUTH TOKEN, TWILIO PHONE NUMBER and MOBILE NUMBER, in your Terminal window export them as environment variables as follows:

    ```
    export ACC_SID='your_account_sid'
    export AUTH_TOKEN='your_auth_token'
    export TWILIO_NUM='your_twilio_phone_number'
    export MOB_NUM='your_mobile_number'
    ```
11. On the consulate's website, there is an optional field 'Nota' for notes that you might want to add to your booking. If you would like this field to be filled, add the following in Terminal:
12. ```
    export NOTA='write_your_note_here'
    ```

    &nbsp;

<h2>RUNNING THE CODE</h2>