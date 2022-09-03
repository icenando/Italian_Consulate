import sys
import time
from os import system

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

from config import my_email, myMobNumber, myTwilioNumber, password, twilioCli
from func_vars import *

########## Start #############

options = webdriver.ChromeOptions()
options.headless = True
#  Launches browswer.
browser = Chrome(executable_path="/usr/local/bin/chromedriver", options=options)
browser.implicitly_wait(2)


class RunChecks:
    def countdown(self, t) -> None:
        for i in range(t, 0, -1):
            sys.stdout.flush()
            if len(str(i)) < 2:
                i = str(f" {i}")
            sys.stdout.write(
                f"\t{i}\r",
            )
            time.sleep(1)

    def __monitor_calendar_changes(self) -> str:
        print(f"<< Checking for no-availability notice >>")
        try:
            browser.find_element_by_css_selector(no_services_popup)
            print(f"<< No availability >>")
            return "no_avail"
        except NoSuchElementException:
            if (
                browser.current_url == "https://prenotami.esteri.it/UserArea"
                or browser.current_url == "https://prenotami.esteri.it"
            ):
                print("<< Automatically logged out. Restarting >>")
                return "logged_out"
        return "dates_available"

    def driver_func(self) -> bool:
        while True:
            calendar_response = self.__monitor_calendar_changes()
            # If still logged in but no free slots are found, refreshes the page before starting again.
            if calendar_response == "no_avail":
                print("<< Awaiting to refresh the page before restarting search >>")
                self.countdown(25)
                print("<< Reloading page >>")
                browser.get(servizi_link)
                prenota_documenti_di_identita(ufficio_passaporti_link)
            elif calendar_response == "logged_out":
                return False
            else:
                print(
                    "<< Available dates! Log in now to check: https://prenotami.esteri.it"
                )
                system(
                    'say "Available dates at the Italian consulate! Log in now to book!'
                )
                message = "Available dates at the Italian Consulate!"
                # Sends the message.
                twilioCli.messages.create(
                    body=message, from_=myTwilioNumber, to=myMobNumber
                )
                self.available_dates = True
                return True


def load_page(url: str) -> None:
    print("<< Loading page >>")
    browser.get(url)
    return None


def fill_in_login_form(
    username: str,
    pw: str,
    login_btn: str,
    my_email: str,
    password: str,
    wrong_pw=False,
) -> bool:
    # Repeat until login is succesful and page changes.
    password = password

    while browser.current_url != "https://prenotami.esteri.it/UserArea":
        browser.find_element_by_css_selector(username).clear()
        if wrong_pw:
            print(
                """
                << Login failed >>\n
                << Please export your credential as follows and relaunch the app: >>\n
                export EMAIL='your_email_goes_here' && export PW='your_password_goes_here'
                """
            )
            return wrong_pw
        browser.find_element_by_css_selector(username).send_keys(my_email)
        browser.find_element_by_css_selector(pw).send_keys(password)
        browser.find_element_by_css_selector(login_btn).click()
        print("<< Filling in the form >>")
        wrong_pw = True
    return False


def prenota_il_servizio(prenota: str) -> None:
    print("<< Navigating to services page >>")
    try:
        browser.find_element_by_css_selector(prenota).click()  # "prenota il servizio".
    except NoSuchElementException:
        return True
    pass


def prenota_documenti_di_identita(prenota_documenti) -> None:
    print("<< Navigating to identity document booking >>")
    try:
        browser.find_element_by_css_selector(ufficio_passaporti_link).click()
    except NoSuchElementException:
        return True
    pass


def main() -> None:
    slot = False
    while not slot:
        load_page(initial_url)

        if fill_in_login_form(  # if login fails
            username_field, pw_field, login_conf_btn, my_email, password
        ):
            browser.quit()
            return None

        # if no 'prenota' link, restart loop
        if prenota_il_servizio(prenotaIlServizio_link):
            continue

        # if no 'prenota' link for identity documents restart loop
        if prenota_documenti_di_identita(ufficio_passaporti_link):
            continue

        slot = RunChecks().driver_func()

    browser.quit()
    return None


if __name__ == "__main__":
    main()
