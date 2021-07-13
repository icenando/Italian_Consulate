#! python3
# config.py - configuration variables for main.py

from twilio.rest import Client  # Twilio.com, for SMS message.
from decouple import UndefinedValueError, config

##### Twilio variables #####
# Open a Twilio account and retrieve the following info.
accountSID = config('ACC_SID')
authToken = config('AUTH_TOKEN')
myTwilioNumber = config('TWILIO_NUM')  # Only US and Canada numbers in the trial account.
myMobNumber = config('MOB_NUM')    # Number that will be receive the SMS notification.
########################

twilioCli = Client(accountSID, authToken)


my_email = config('EMAIL')
password = config('PW')

# Optional field 'Nota' on Italian Consulate website
try: 
    nota = config('NOTA')
except UndefinedValueError:
    nota = ''