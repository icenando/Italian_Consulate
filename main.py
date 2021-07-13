from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

import sys
# import os
from datetime import datetime
import time

from config import twilioCli, myTwilioNumber, myMobNumber, twilioCli, my_email, password
from func_vars import *


# Start of programme

# start_time = time.perf_counter()
options = webdriver.ChromeOptions()
options.headless=True
browser = Chrome(executable_path='/usr/local/bin/chromedriver', options=options)  # Launches browswer.
browser.implicitly_wait(2)



class RunChecks():
    available_dates = []

    def countdown(self, t) -> None:
        for i in range(t, 0, -1):
                sys.stdout.flush()
                if len(str(i)) < 2:
                    i = str(f" {i}")
                sys.stdout.write (f'\t{i}\r',)
                time.sleep(1)


    def parse_dates(self) -> str:
            months_dict = {
                'gennaio': '01',
                'febbraio': '02',
                'marzo': '03',
                'aprile': '04',
                'maggio': '05',
                'giugno': '06',
                'luglio': '07',
                'agosto': '08',
                'settembre': '09',
                'ottobre': '10',
                'novembre': '11',
                'dicembre': '12'
            }

            for i in range(len(self.available_dates)):
                day = self.available_dates[i][0]
                month = months_dict[self.available_dates[i][1][:-5]]
                year = self.available_dates[i][1][-4:]
                self.available_dates[i] = '/'.join([day, month, year])
                # Converts to datetime for sorting
                self.available_dates[i] = datetime.strptime(self.available_dates[i], '%d/%m/%Y')
                
            self.available_dates.sort()
            # Converts back to str
            for i in range(len(self.available_dates)):
                self.available_dates[i] = datetime.strftime(self.available_dates[i], '%d/%m/%Y')

            return ', '.join(self.available_dates)


    def driver_func(self) -> bool:

        while not self.available_dates:
            for time_of_day, am_pm in enumerate(ufficio_passaporti_links):
                self.__passaporto_am_pm(am_pm)

                calendar_response = self.__monitor_calendar_changes(time_of_day)
                if calendar_response == "logged_out":
                    return False
                # If still logged in but no free slots are found, refreshes the page before starting again.
                elif calendar_response == "no_avail_pm":
                    print("<< Awaiting to refresh the page before restarting search >>")
                    # end_time = time.perf_counter()
                    # print(end_time - start_time)
                    self.countdown(25)
                    print("<< Reloading page >>")
                    browser.get(servizi_link)

        # Sends the message.
        message = "Available dates at the Italian Consulate" + self.parse_dates()
        twilioCli.messages.create(body=message, from_=myTwilioNumber, to=myMobNumber)

        return True


    def __passaporto_am_pm(self, am_pm: str) -> None:       
        browser.find_element_by_css_selector(am_pm).click()  # "passaporto".
        browser.find_element_by_css_selector(privacy_check).click()  # Checks privavy checkbox.
        browser.find_element_by_css_selector(conferma_btn).click()

        return None


    def __monitor_calendar_changes(self, time_of_day: str) -> str:
        if time_of_day == 0:
            time_of_day = 'am'
        else: time_of_day = "pm"
        print(f"<< Searching ({time_of_day}) calendar for available appointment slots >>")

        # Tries to find calender:
        try:
            current_calendar = browser.find_element_by_css_selector(calendar_selector)
        except NoSuchElementException:
            # If no calendar, checks if there's 'no availability' pop up.
            try:
                browser.find_element_by_css_selector(no_services_popup)
            except NoSuchElementException:
                print("<< Automatically logged out. Restarting >>")
                return "logged_out"

            # If there is a 'no availability' pop up.
            print(f"<< No availability ({time_of_day}) >>")
            if time_of_day == "pm":
                return "no_avail_pm"
            # Loads the 'servizi' page, where am and pm links are
            browser.get(servizi_link)
            return ''

        # After checks, if the calendar is in the page.
        two_months_ahead = 0
        while two_months_ahead <= 2:
            checking_month = browser.find_element_by_css_selector(current_month).text
            print(f"<< Checking month: {checking_month} >>")
            print("<< Checking days: ", end= '')
            # Iterates through weeks.
            for week in current_calendar.find_elements_by_css_selector('tr'):
                # Iterates through the days of that week.
                for day in week.find_elements_by_tag_name('td'):
                    checking_day = day.text
                    print(checking_day, end=' ')
                    # If available day.
                    if day.get_attribute("class") not in day_status:
                        print(' >>\n')
                        slot_date = ' '.join([checking_day, checking_month])
                        message = "Available slot: " + slot_date + time_of_day
                        print(f"\n<< **** {message} **** >>\n\n")
                        self.available_dates.append([checking_day, checking_month])
                        return None

            # If no slots found.    
            print(' >>')
            print(f"<< No available slots in {checking_month} >>\n")
            # Advances the calendar to next month.
            if two_months_ahead < 2:
                browser.find_element_by_css_selector(next_month_cal).click()
            two_months_ahead += 1

        # No slots found in the current month and next two months.
        return None


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
        ) -> bool:
    # Repeat until login is succesful and page changes.
    password = password

    while browser.current_url != "https://prenotami.esteri.it/UserArea":
        browser.find_element_by_css_selector(username).clear()
        if wrong_pw:
            print("""
                << Login failed >>\n
                << Please export your credential as follows and relaunch the app: >>\n
                export EMAIL='your_email_goes_here' && export PW='your_password_goes_here'
                """)
            return wrong_pw
        browser.find_element_by_css_selector(username).send_keys(my_email)
        browser.find_element_by_css_selector(pw).send_keys(password)
        browser.find_element_by_css_selector(login_btn).click()
        print('<< Filling in the form >>')
        wrong_pw = True
    return False


def prenota_il_servizio(prenota: str) -> None:
    print("<< Navigating to services page >>")
    try:
        browser.find_element_by_css_selector(prenota).click()  # "prenota il servizio".
    except NoSuchElementException:
        return True
    pass


def main() -> None:
    slot = False
    while not slot:
        load_page(initial_url)

        if fill_in_login_form(  # if login fails
                username_field, 
                pw_field, 
                login_conf_btn, 
                my_email, 
                password
                ):
            browser.quit()
            return None
        
        if prenota_il_servizio(prenotaIlServizio_link):  #if no 'prenota' link
            continue
        run_checks = RunChecks()
        slot = run_checks.driver_func()

        # end_time = time.perf_counter()
        # print(start_time - end_time)

    browser.quit()
    return None

if __name__ == '__main__':
    main()