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
servizi_link = "https://prenotami.esteri.it/Services"  # Here is where the am or pm links are
ufficio_passaporti_link_am = "#dataTableServices > tbody > tr:nth-child(5) > td:nth-child(4) > a > button"
ufficio_passaporti_link_pm = "#dataTableServices > tbody > tr:nth-child(6) > td:nth-child(4) > a > button"
ufficio_passaporti_links = [ufficio_passaporti_link_am, ufficio_passaporti_link_pm]
no_services_popup = "body > div.jconfirm.jconfirm-light.jconfirm-open"
nota_css = "#BookingNotes"
privacy_check = "#PrivacyCheck"
conferma_btn = "#submit"

# monitorCalendarChanges()
next_month_cal = "#datetimepicker > div > ul > ul > div > div.datepicker-days > table > thead > tr:nth-child(1) > th.dtpicker-next > span"
calendar_selector = "#datetimepicker > div > ul > ul > div > div.datepicker-days > table > tbody"
current_month = "#datetimepicker > div > ul > ul > div > div.datepicker-days > table > thead > tr:nth-child(1) > th.picker-switch"
day_status = [
    'day old disabled',
    'day old weekend disabled',
    'day disabled notAvailableDay active',
    'day disabled',
    'day weekend disabled',
    'day new disabled',
    'day new weekend disabled',
    'day disabled notAvailableDay',
    'day active today disabled'
    ]

###############################
###############################
