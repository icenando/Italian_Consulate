from config import twilioCli, myTwilioNumber, myMobNumber, twilioCli, my_email, password
from func_vars import *

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

# from os import system  # Just for the voice alert.
import time  # Delays to allow website to load all elements.
from pyinputplus import inputPassword # To hide password during input.
import sys
import os

# Start of programme

def load_page(url: str) -> None:
    print('<< Loading page >>')
    browser.get(url)
    return None


def fill_in_login_form(
        username: str, 
        pw: str, 
        login_btn: str, 
        my_email: str,
        password: str,
        wrong_pw = False,
        ) -> None:
    # Repeat until login is succesful and page changes.
    password = password

    while browser.current_url != "https://prenotami.esteri.it/UserArea":
        browser.find_element_by_css_selector(username).clear()
        if wrong_pw:
            print("<< Login failed. Please enter your email and password again >>")
        # print("Enter email HERE: ", end='')
        # my_email = input()
        browser.find_element_by_css_selector(username).send_keys(my_email)
        # password = inputPassword("Enter password HERE: ")
        browser.find_element_by_css_selector(pw).send_keys(password)
        browser.find_element_by_css_selector(login_btn).click()
        print('<< Filling in the form >>')
        usr_name, password = '',''
        wrong_pw = True
    return None


def prenota_il_servizio(
            prenota: str, 
            passp: str, 
            nota: str, 
            priv_check: str, 
            conf_btn: str
            ) -> None:
    print("<< Navigating to services page >>")
    delay = 1
    browser.find_element_by_css_selector(prenota).click()  # "prenota il servizio".
    time.sleep(delay)
    browser.find_element_by_css_selector(passp).click()  # "passaporto".
    time.sleep(delay)

    #TODO: Prenotazione singola / multipla
    if os.getenv('NOTA') != None:
        browser.find_element_by_css_selector(nota).send_keys(os.environ['NOTA'])  # Optional "Nota" field.
    browser.find_element_by_css_selector(priv_check).click()  # Checks privavy checkbox.
    browser.find_element_by_css_selector(conf_btn).click()
    return None


def monitor_calendar_changes(next_month: str, calendar: str, day_status: list, current_month: str) -> None:
    print("<< Searching calendar for available appointment slots >>")
    slot = False
    
    # Repeats until a free slot is found.
    while not slot:
        try:
            current_calendar = browser.find_element_by_css_selector(calendar)
        except NoSuchElementException:
            print("<< Automatically logged out >>")
            # system('say "You have been logged out. Relaunch the programme."')
            return None

        two_months_ahead = 0
        while two_months_ahead <= 2:
            checking_month = browser.find_element_by_css_selector(current_month).text
            print(f"<< Checking month: {checking_month} >>")
            print("<< Checking days: ", end= '')
            for week in current_calendar.find_elements_by_css_selector('tr'):   # Iterates through weeks.
                for day in week.find_elements_by_tag_name('td'):  # Iterates through the days of that week.
                    checking_day = day.text
                    print(checking_day, end=' ')
                    if day.get_attribute("class") not in day_status:
                        print(day.get_attribute("class"))
                        print(' >>\n\n')
                        message = "Available slot: " + ' '.join([checking_day, checking_month]) + ' am'
                        print(f"\n\n<< **** {message} ****>>\n\n")
                        # Sends the message.
                        # twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myMobNumber)
                        slot = True
                        return None
            print(' >>')
            print(f"<< No available slots in {checking_month} >>\n")
            # Advances the calendar to next month.
            browser.find_element_by_css_selector(next_month).click()
            two_months_ahead += 1
            time.sleep(2)

        if not slot:  # If no free slots are found, refreshes the page before looking for free slots again.
            print("<< Awaiting to refresh the page before restarting search >>")
            for i in range(25, 0, -1):
                sys.stdout.flush()
                if len(str(i)) < 2:
                    i = str(f" {i}")
                sys.stdout.write (f'\t{i}\r',)
                time.sleep(1)
            
            print("<< Reloading page >>")
            browser.refresh()
            time.sleep(2)

    return None


if __name__ == '__main__':
    browser = Chrome(executable_path='/usr/local/bin/chromedriver')  # Launches browswer.
    time.sleep(2)

    load_page(initial_url)
    time.sleep(2)

    fill_in_login_form(
        username_field, 
        pw_field, 
        login_conf_btn, 
        my_email, 
        password
        )
    time.sleep(1.5)
    
    prenota_il_servizio(
        prenotaIlServizio_link, 
        ufficio_passaporti_link_am, 
        nota_css, 
        privacy_check, 
        conferma_btn)
    time.sleep(1)

    monitor_calendar_changes(
        next_month_cal, 
        calendar_selector, 
        day_status, 
        current_month
        )

    browser.quit()