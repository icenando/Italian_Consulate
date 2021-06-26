#! python3
# config.py - configuration variables for main.py

from twilio.rest import Client  # Twilio.com, for SMS message.
import os
from selenium.webdriver import Chrome

##### Twilio variables #####
# Open a Twilio account and retrieve the following info.
accountSID = os.environ['ACC_SID']
authToken = os.environ['AUTH_TOKEN']
myTwilioNumber = os.environ['TWILIO_NUM']  # Only US and Canada numbers in the trial account.
myMobNumber = os.environ['MOB_NUM']    # Number that will be receive the SMS notification.
########################

twilioCli = Client(accountSID, authToken)
