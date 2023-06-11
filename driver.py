from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from config import BaseDriver, URL, \
    STEAM_LOGIN_BUTTON_XPATH, STEAM_USERNAME_INPUT_XPATH, STEAM_PASSWORD_INPUT_XPATH, \
    STEAM_LOGIN_BUTTON_START_XPATH, STEAM_LOGIN_ERROR, STEAM_FINAL_LOGIN_BUTTON_XPATH

from config import SKIN_NAME_XPATH, SKIN_PRICE_XPATH, SKIN_STICKERS_XPATH, SKIN_VIEW_IN_3D_XPATH, SKIN_IFRAME_XPATH, \
    SKIN_FLOT_XPATH, SKIN_PATTERN_BUTTON_XPATH, SKIN_PATTERN_LIST_XPATH, SKIN_PATTERN_XPATH

from config import CLOUD_FLARE_XPATH, CLOUD_FLARE_IFRAME_XPATH, SKIN_PRICE_ERROR_XPATH

from config import SKIN_ITEMS_LINK

from config import FAST_SKIN_PATTERN_XPATH, FAST_SKIN_FLOAT_XPATH

from time import sleep
from tqdm import tqdm
import random


class Driver(BaseDriver):
    def log_in(self, username: str, password: str) -> bool:
        print('Обход Защиты')
        self.get(URL)

        iter_request = 0

        while True:
            try:
                if iter_request == 10:
                    iter_request = 0
                    self.get(URL)
                iter_request += 1
                self.switch_to.frame(self.find_element(By.XPATH, CLOUD_FLARE_IFRAME_XPATH))
                self.find_element(By.XPATH, CLOUD_FLARE_XPATH).click()
            except (NoSuchElementException, WebDriverException):
                if self.driver_sleep(int(random.random() * 10), STEAM_LOGIN_BUTTON_START_XPATH):
                    break

        print('Вход в аккаунт')
        self.find_element(By.XPATH, STEAM_LOGIN_BUTTON_START_XPATH).click()

        self.driver_sleep(60, STEAM_USERNAME_INPUT_XPATH)
        self.find_element(By.XPATH, STEAM_USERNAME_INPUT_XPATH).send_keys(username)
        self.find_element(By.XPATH, STEAM_PASSWORD_INPUT_XPATH).send_keys(password)
        self.find_element(By.XPATH, STEAM_LOGIN_BUTTON_XPATH).click()

        self.driver_sleep(5, STEAM_FINAL_LOGIN_BUTTON_XPATH)
        try:
            self.find_element(By.XPATH, STEAM_LOGIN_ERROR)
            return False
        except NoSuchElementException:
            self.driver_sleep(20, STEAM_FINAL_LOGIN_BUTTON_XPATH)
            self.find_element(By.XPATH, STEAM_FINAL_LOGIN_BUTTON_XPATH).click()
            return True

    def get_items_url(self) -> None:
        items = self.find_element(By.XPATH, SKIN_ITEMS_LINK).find_elements(By.TAG_NAME, 'a')
        for item in items:
            try:
                item.find_element(By.CLASS_NAME, 'mat-mdc-tooltip-trigger')
                self.fast_items_link.append(item.get_attribute('href'))
            except NoSuchElementException:
                self.items_link.append(item.get_attribute('href'))

    def base_pars_data(self, url: str) -> [dict, bool]:
        data = {}

        self.get(url)

        if self.driver_sleep(10, SKIN_NAME_XPATH):
            data['name'] = self.find_element(By.XPATH, SKIN_NAME_XPATH).text
        else:
            return False

        try:
            data['price'] = str(self.find_element(By.XPATH, SKIN_PRICE_XPATH).text)
        except NoSuchElementException:
            try:
                self.find_element(By.XPATH, SKIN_PRICE_ERROR_XPATH)
                return False
            except NoSuchElementException:
                data['price'] = 'error'

        if self.driver_sleep(5, SKIN_STICKERS_XPATH):
            data['stickers'] = ''
            for skin in self.find_element(By.XPATH, SKIN_STICKERS_XPATH).find_elements(By.TAG_NAME, 'a'):
                data['stickers'] += skin.get_attribute('title') + ','
        else:
            data['stickers'] = 'none'

        data['url'] = url

        return data

    def fast_items_pars(self, url: str) -> [dict, bool]:
        data = self.base_pars_data(url)

        if data is False:
            return False

        try:
            self.driver_sleep(15, FAST_SKIN_PATTERN_XPATH)
            data['pattern'] = self.find_element(By.XPATH, FAST_SKIN_PATTERN_XPATH).text
        except NoSuchElementException:
            data['pattern'] = 'error'

        try:
            self.driver_sleep(15, FAST_SKIN_FLOAT_XPATH)
            data['float'] = self.find_element(By.XPATH, FAST_SKIN_FLOAT_XPATH).text.split(' ')[0]
        except NoSuchElementException:
            data['float'] = 'Item with specified asset not found'

        return data

    def parse_data(self, url: str) -> [dict, bool]:
        data = self.base_pars_data(url)

        if data is False:
            return False

        try:
            self.find_element(By.XPATH, SKIN_VIEW_IN_3D_XPATH).click()
            self.driver_sleep(15, SKIN_IFRAME_XPATH)
        except NoSuchElementException:
            data['pattern'] = 'error'
            data['float'] = 'Item with specified asset not found'
            return False

        try:
            self.switch_to.frame(self.find_element(By.XPATH, SKIN_IFRAME_XPATH))
            self.driver_sleep(15, SKIN_FLOT_XPATH)
            data['float'] = self.find_element(By.XPATH, SKIN_FLOT_XPATH).text
        except NoSuchElementException:
            data['float'] = 'Item with specified asset not found'

        wait = WebDriverWait(self, 5)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, SKIN_PATTERN_BUTTON_XPATH)))
            self.find_element(By.XPATH, SKIN_PATTERN_BUTTON_XPATH).click()

            wait.until(EC.element_to_be_clickable((By.XPATH, SKIN_PATTERN_LIST_XPATH)))
            self.find_element(By.XPATH, SKIN_PATTERN_LIST_XPATH).click()

            sleep(7)
            data['pattern'] = self.find_element(By.XPATH,
                                                SKIN_PATTERN_XPATH).find_element(By.CLASS_NAME,
                                                                                 'is-selected').text.split('#')[-1]
        except (NoSuchElementException, TimeoutException):
            data['pattern'] = 'error'

        return data

    def parsing_skins(self, skins_list: list) -> None:
        print('парсинг скинов')
        for skin_link in tqdm(skins_list):
            data = self.parse_data(skin_link)

            if data:
                self.skins_data.append(data)

            print(data)

            self.switch_to.default_content()
            self.get_items_url()

    def parsing_items(self) -> None:
        print(f'парсинг предметов\n предметов: {len(self.fast_items_link) + len(self.items_link)}')

        for item_link in tqdm(self.fast_items_link):
            data = self.fast_items_pars(item_link)
            if data:
                self.items_data.append(data)
                print(data)

        for item_link in tqdm(self.items_link):
            data = self.parse_data(item_link)
            if data:
                self.items_data.append(data)
                print(data)
