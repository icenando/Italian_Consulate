#! python3
# func_vars.py - declaration of all text variables used in main.py

##### FUNCTION VARIABLES ######
###############################

# loadPage()
initial_url = "https://prenotami.esteri.it"  # Initial URL.

# fillInLoginForm()
username_field = "#login-email"
pw_field = "#login-password"
login_conf_btn = "#login-form > button"

# prenotaIlServizio()
prenotaIlServizio_link = "#advanced > span"
servizi_link = "https://prenotami.esteri.it/Services"
ufficio_passaporti_link = (
    "#dataTableServices > tbody > tr:nth-child(2) > td:nth-child(4) > a > button"
)
no_services_popup = "body > div.jconfirm.jconfirm-light.jconfirm-open"

###############################
###############################
