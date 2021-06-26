from config import twilioCli, myTwilioNumber, myMobNumber, twilioCli
from func_vars import *

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

from os import system  # Just for the voice alert.
import time  # Delays to allow website to load all elements.



# Start of programme

def load_page(url: str, button: str) -> None:
    browser.get(url)
    time.sleep(3)
    browser.find_element_by_css_selector(button).click()
    return None


def fill_in_login_form(username: str, pw: str, capt_field: str, login_btn: str) -> None:
    # Repeat until login is succesful and page changes.
    while browser.current_url != "https://prenotaonline.esteri.it/default.aspx":
        browser.find_element_by_css_selector(username).clear()
        print("Enter username HERE: ", end='')
        usr_name = input()
        browser.find_element_by_css_selector(username).send_keys(usr_name)
        print("Enter password HERE: ", end = '')
        password = input()
        browser.find_element_by_css_selector(pw).send_keys(password)
        print("Enter captcha HERE: ", end='')
        captcha = input()
        browser.find_element_by_css_selector(capt_field).send_keys(captcha)
        browser.find_element_by_css_selector(login_btn).click()
        time.sleep(1)
    return None


def prenota_il_servizio(prenota: str, passp: str, nota: str, conf_btn: str) -> None:
    delay = 2
    browser.find_element_by_css_selector(prenota).click()  # "prenota il servizio".
    time.sleep(delay)
    browser.find_element_by_css_selector(passp).click()  # "passaporto".
    time.sleep(delay)
    browser.find_element_by_css_selector(nota).send_keys(nota)  # Optional field.
    time.sleep(1)
    browser.find_element_by_css_selector(conf_btn).click()
    return None


def monitor_calendar_changes(next_month: str, calendar: str) -> None:
    slot = False

    # Advances the calendar by one month (current month is always fully-booked).
    browser.find_element_by_css_selector(next_month).click()
    
    # Repeats until a free slot is found.
    while not slot:
        try:
            current_calendar = browser.find_element_by_css_selector(calendar)
        except NoSuchElementException:
            print("Kicked out.")
            system('say "You have been logged out. Relaunch the programme."')
            return None
        for week in current_calendar.find_elements_by_css_selector('tr'):   # Iterates through weeks.
            for day in week.find_elements_by_tag_name('td'):  # Iterates through the days of that week.
                # These are the only two texts when no slots are free.
                if day.get_attribute("title") != "Giorno non disponibile" and \
                            day.get_attribute("title") != "Tutto occupato":
                    available_slot_month = current_calendar.find_element_by_tag_name("span").text
                    print("Available slot in: ", available_slot_month)
                    system('say "The Italian Consulate might have a free spot!"')
                    sms_text = "Italian Consulate free slot in: " + available_slot_month
                    print(sms_text)
                    # Sends the message.
                    twilioCli.messages.create(body=sms_text, from_=myTwilioNumber, to=myMobNumber)
                    slot = True
                    return None
        if not slot:  # If no free slots are found, refreshes the page before looking for free slots again.
            time.sleep(25)
            browser.refresh()
            time.sleep(3)
    return None


if __name__ == '__main__':
    browser = Chrome(executable_path='/usr/local/bin/chromedriver')  # Launches browswer.
    time.sleep(2)

    load_page(initial_url, login_button)
    time.sleep(1)

    fill_in_login_form(username_field, pw_field, captcha_field, login_conf_btn)
    time.sleep(1.5)
    
    prenota_il_servizio(prenotaIlServizio_link, ufficio_passaporti_link, nota_css, conferma_btn)
    time.sleep(1)

    monitor_calendar_changes(next_month_cal, calendar_selector)
