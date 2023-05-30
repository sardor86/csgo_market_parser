from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from config import BaseDriver, URL, \
                   STEAM_LOGIN_BUTTON_XPATH, STEAM_USERNAME_INPUT_XPATH, STEAM_PASSWORD_INPUT_XPATH, \
                   STEAM_LOGIN_BUTTON_START_XPATH, STEAM_LOGIN_ERROR, STEAM_FINAL_LOGIN_BUTTON_XPATH

from config import SKIN_NAME_XPATH, SKIN_PRICE_XPATH, SKIN_STICKERS_XPATH, SKIN_VIEW_IN_3D_XPATH, SKIN_IFRAME_XPATH, \
                   SKIN_FLOT_XPATH, SKIN_PATTERN_BUTTON_XPATH, SKIN_PATTERN_LIST_XPATH, SKIN_PATTERN_XPATH

from config import PAGE_404_XPATH, CLOUD_FLARE_XPATH, CLOUD_FLARE_IFRAME_XPATH, SKIN_PRICE_ERROR_XPATH

from config import SKIN_ITEMS_LINK

from time import sleep
from tqdm import tqdm


class Driver(BaseDriver):
    def log_in(self, username: str, password: str) -> bool:
        print('Обход Защиты')
        self.get(URL)
        sleep(10)
        try:
            self.switch_to.frame(self.find_element(By.XPATH, CLOUD_FLARE_IFRAME_XPATH))
            self.find_element(By.XPATH, CLOUD_FLARE_XPATH).click()
        except NoSuchElementException:
            pass

        print('Вход в аккаунт')
        self.wait.until(EC.presence_of_element_located((By.XPATH, STEAM_LOGIN_BUTTON_START_XPATH)))
        self.find_element(By.XPATH, STEAM_LOGIN_BUTTON_START_XPATH).click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, STEAM_USERNAME_INPUT_XPATH)))
        self.find_element(By.XPATH, STEAM_USERNAME_INPUT_XPATH).send_keys(username)
        self.find_element(By.XPATH, STEAM_PASSWORD_INPUT_XPATH).send_keys(password)
        self.find_element(By.XPATH, STEAM_LOGIN_BUTTON_XPATH).click()

        self.wait.until(EC.presence_of_element_located((By.XPATH, STEAM_FINAL_LOGIN_BUTTON_XPATH)))
        try:
            self.find_element(By.XPATH, STEAM_LOGIN_ERROR)
            return False
        except NoSuchElementException:
            self.find_element(By.XPATH, STEAM_FINAL_LOGIN_BUTTON_XPATH).click()
            return True

    def parsing_skins(self, skins_list: list) -> None:
        print('парсинг скинов')
        for skin_link in tqdm(skins_list):
            skin_data = []

            self.get(skin_link)
            self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_NAME_XPATH)))
            sleep(5)

            try:
                self.find_element(By.XPATH, PAGE_404_XPATH)
                self.skins_data.append(None)
                continue
            except:
                pass

            skin_data.append(self.find_element(By.XPATH, SKIN_NAME_XPATH).text)

            try:
                skin_data.append(str(self.find_element(By.XPATH, SKIN_PRICE_XPATH).text))
            except:
                try:
                    self.find_element(By.XPATH, SKIN_PRICE_ERROR_XPATH)
                    continue
                except:
                    skin_data.append('error')

            try:
                skin_data.append([])
                for skin in self.find_element(By.XPATH, SKIN_STICKERS_XPATH).find_elements(By.TAG_NAME, 'a'):
                    skin_data[-1].append(skin.get_attribute('title'))
            except:
                skin_data[-1] = 'none'

            try:
                self.find_element(By.XPATH, SKIN_VIEW_IN_3D_XPATH).click()
                self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_IFRAME_XPATH)))
            except:
                skin_data.append('none')
                skin_data.append('none')
                continue

            sleep(15)
            try:
                self.switch_to.frame(self.find_element(By.XPATH, SKIN_IFRAME_XPATH))
                self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_FLOT_XPATH)))
                skin_data.append(self.find_element(By.XPATH, SKIN_FLOT_XPATH).text)

                self.find_element(By.XPATH, SKIN_PATTERN_BUTTON_XPATH).click()
                sleep(.5)

                self.find_element(By.XPATH, SKIN_PATTERN_LIST_XPATH).click()
                sleep(.5)
                skin_data.append(self.find_element(By.XPATH,
                                                   SKIN_PATTERN_XPATH).find_element(By.CLASS_NAME,
                                                                                    'is-selected').text.split('#')[-1])
            except:
                skin_data.append('Item with specified asset not found')
                skin_data.append('Item with specified asset not found')
                continue
            finally:
                skin_data.append(skin_link)
                self.skins_data.append(skin_data)

                self.switch_to.default_content()

                for item_link in self.find_element(By.XPATH, SKIN_ITEMS_LINK).find_elements(By.TAG_NAME, 'a'):
                    self.items_link.append(item_link.get_attribute('href'))

    def parsing_items(self) -> None:
        print('парсинг скинов')
        for item_link in tqdm(self.items_link):
            item_data = []

            self.get(item_link)
            self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_NAME_XPATH)))
            sleep(5)

            try:
                self.find_element(By.XPATH, PAGE_404_XPATH)
                self.skins_data.append(None)
                continue
            except:
                pass

            item_data.append(self.find_element(By.XPATH, SKIN_NAME_XPATH).text)

            try:
                item_data.append(str(self.find_element(By.XPATH, SKIN_PRICE_XPATH).text))
            except:
                try:
                    self.find_element(By.XPATH, SKIN_PRICE_ERROR_XPATH)
                    continue
                except:
                    item_data.append('error')

            try:
                item_data.append([])
                for skin in self.find_element(By.XPATH, SKIN_STICKERS_XPATH).find_elements(By.TAG_NAME, 'a'):
                    item_data[-1].append(skin.get_attribute('title'))
            except:
                item_data[-1] = 'none'

            try:
                self.find_element(By.XPATH, SKIN_VIEW_IN_3D_XPATH).click()
                self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_IFRAME_XPATH)))
            except:
                item_data.append('none')
                item_data.append('none')
                continue

            sleep(15)
            try:
                self.switch_to.frame(self.find_element(By.XPATH, SKIN_IFRAME_XPATH))
                self.wait.until(EC.presence_of_element_located((By.XPATH, SKIN_FLOT_XPATH)))
                item_data.append(self.find_element(By.XPATH, SKIN_FLOT_XPATH).text)

                self.find_element(By.XPATH, SKIN_PATTERN_BUTTON_XPATH).click()
                sleep(.5)

                self.find_element(By.XPATH, SKIN_PATTERN_LIST_XPATH).click()
                sleep(.5)
                item_data.append(self.find_element(By.XPATH,
                                                   SKIN_PATTERN_XPATH).find_element(By.CLASS_NAME,
                                                                                    'is-selected').text.split('#')[-1])
            except:
                item_data.append('Item with specified asset not found')
                item_data.append('Item with specified asset not found')

            self.items_data.append(item_data)
