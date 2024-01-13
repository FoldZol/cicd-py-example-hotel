import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import allure
import pytest
import random


class TestHootel(object):
    def setup_method(self):
        URL = 'http://hotel-v3.progmasters.hu/'
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    @pytest.mark.parametrize("email, password", [('progmtest4@proton.me', 'ProgMtest4')])
    @allure.title("Hootel Login")
    @allure.description("A belépés tesztelése")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("login")
    def test_login(self, email, password):
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email)

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()

        logout_btn = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "logout-link")))

        assert logout_btn.text == "Kilépés"

    def test_hotel_list(self):
        hotel_list_btn = self.browser.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        time.sleep(1)

        hotel_list = self.browser.find_elements(By.XPATH, '//h4[@style="cursor: pointer"]')
        assert len(hotel_list) != 0
        assert len(hotel_list) == 10

    def test_hotel_description_rule(self):
        # random hotel kiválasztása és adatlapjának megnyitása
        hotel_list_btn = self.browser.find_element(By.XPATH, "//button[text()=' Megnézem a teljes listát ']")
        hotel_list_btn.click()
        hotels = WebDriverWait(self.browser, 5).until(
            ec.presence_of_all_elements_located((By.XPATH, "//button[text() = 'Megnézem']")))
        random.choice(hotels).click()

        # description begyűjtése
        # time.sleep nélkül 2 elemet gyűjtött be a WebDriverWait mivel, amit talált az igazzá tette a presence of all elements-et. Emiatt force-ni kell a time.sleep-et.
        time.sleep(1)
        description = WebDriverWait(self.browser, 5).until(
            ec.presence_of_all_elements_located((By.XPATH, f"//p[@class='card-text']")))[1].text

        assert len(description) >= 500

    def test_logout(self):
        # bejelentkezés
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_button = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_button.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys('progmtest4@proton.me')

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys('ProgMtest4')

        submit_button = self.browser.find_element(By.NAME, 'submit')
        submit_button.click()

        # kijelentkezés
        logout_button = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "logout-link")))
        logout_button.click()

        # sikeres kijelentkezés ellenőrzése
        login_button = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))

        assert login_button.text == "Bejelentkezés"

    def test_user_booking_button(self):
        # bejelentkezés
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_button = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_button.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys('progmtest4@proton.me')

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys('ProgMtest4')

        submit_button = self.browser.find_element(By.NAME, 'submit')
        submit_button.click()

        # foglalások oldalra navigálás
        bookings_btn = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//a[@id = 'user-bookings']")))
        bookings_btn.click()

        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler']")))
        menu_toggle.click()

        # oldal betöltésének ellenőrzése
        assert self.browser.current_url == "http://hotel-v3.progmasters.hu/bookings"

    def test_user_profile_button(self):
        # bejelentkezés
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_button = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_button.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys('progmtest4@proton.me')

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys('ProgMtest4')

        submit_button = self.browser.find_element(By.NAME, 'submit')
        submit_button.click()

        # felhasználói fiók oldalra való navigálás
        account_button = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "profile")))
        account_button.click()

        # oldal betöltésének ellenőrzése
        assert self.browser.current_url == "http://hotel-v3.progmasters.hu/account"

    def test_editing_user_account(self):
        # bejelentkezés
        menu_toggle = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@class = 'navbar-toggler collapsed']")))
        menu_toggle.click()
        login_button = WebDriverWait(self.browser, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_button.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys('progmtest4@proton.me')

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys('ProgMtest4')

        submit_button = self.browser.find_element(By.NAME, 'submit')
        submit_button.click()

        # felhasználói fiók oldalra való navigálás
        account_button = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "profile")))
        account_button.click()

        account_former_lastname = WebDriverWait(self.browser, 5).until(ec.presence_of_element_located((By.XPATH, "//input[@id = 'firstname']"))).text
                                                                                                       
        edit_account_button = self.browser.find_element(By.XPATH, "//button[@name = 'submit']")
        edit_account_button.click()

        lastname_input = self.browser.find_element(By.ID, "firstname")
        lastname_input.send_keys("ProgMtest4")

        save_button = WebDriverWait(self.browser, 5).until(ec.element_to_be_clickable((By.ID, "submit")))
        save_button.click()

        account_changed_lastname = WebDriverWait(self.browser, 5).until(ec.presence_of_element_located((By.XPATH, "//input[@id = 'firstname']"))).text

        assert account_former_lastname != account_changed_lastname

        
        
