#! python3
# func_vars.py - declaration of all text variables used in main.py

##### FUNCTION VARIABLES ######
###############################

# loadPage()
initial_url = "https://prenotaonline.esteri.it/Login.aspx?cidsede=100041&returnUrl=%2f%2f"  # Initial URL.
login_button = "#BtnLogin"

# fillInLoginForm()
username_field = "#UserName"
pw_field = "#Password"
captcha_field = "#loginCaptcha"
login_conf_btn = "#BtnConfermaL"

# prenotaIlServizio()
prenotaIlServizio_link = "#ctl00_repFunzioni_ctl00_btnMenuItem"
ufficio_passaporti_link = "#ctl00_ContentPlaceHolder1_rpServizi_ctl04_btnNomeServizio"
nota_css = "#ctl00_ContentPlaceHolder1_acc_datiAddizionali1_txtNote"
conferma_btn = "#ctl00_ContentPlaceHolder1_acc_datiAddizionali1_btnContinua"

# monitorCalendarChanges()
next_month_cal = "#ctl00_ContentPlaceHolder1_acc_Calendario1_myCalendario1 > table > tbody > tr.calTitolo > th:nth-child(3) > input"
calendar_selector = "#ctl00_ContentPlaceHolder1_acc_Calendario1_myCalendario1 > table > tbody"

###############################
###############################
