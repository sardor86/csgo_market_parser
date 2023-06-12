import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pathlib import Path

PATH = Path(__file__).parent

BROWSER_SETTINGS = 'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                   'Chrome/51.0.2704.103 Safari/537.36'

URL = 'https://market.csgo.com/'

CLOUD_FLARE_IFRAME_XPATH = '/html/body/div[1]/div/div[1]/div/div/iframe'
CLOUD_FLARE_XPATH = '/html/body/table/tbody/tr/td/div/div[1]/table/tbody/tr/td[1]/div[1]/div/label/input'

STEAM_LOGIN_BUTTON_START_XPATH = '/html/body/app-root/div/app-main-site/app-header/div/div/div[2]/div/button'
STEAM_USERNAME_INPUT_XPATH = '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input'
STEAM_PASSWORD_INPUT_XPATH = '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input'
STEAM_LOGIN_BUTTON_XPATH = '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button'
STEAM_LOGIN_ERROR = '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[5]'
STEAM_FINAL_LOGIN_BUTTON_XPATH = '/html/body/div[1]/div[7]/div[2]/div/div[2]/div[2]/div/form/input[5]'

SKIN_NAME_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/div/' \
                   'app-page-inventory-info-wrap/div/app-full-item-info/div/h1/span'
SKIN_PRICE_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/div/' \
                   'app-page-inventory-info-wrap/div/div[1]/div/span[1]'
SKIN_STICKERS_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/div/' \
                      'app-page-inventory-info-wrap/div/app-full-item-info/div/div[2]/app-full-item-info-stickers'
SKIN_VIEW_IN_3D_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/' \
                        'div/app-page-inventory-image/div/div/div[2]/div[1]/button'
SKIN_IFRAME_XPATH = '/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/' \
                    'app-custom-component/app-modal-wrap/app-show3d/iframe'
SKIN_FLOT_XPATH = '/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/span[5]'
SKIN_PATTERN_BUTTON_XPATH = '/html/body/div/div/div/div/header/div/div/div/div/div/button'
SKIN_PATTERN_LIST_XPATH = '/html/body/div/div/div/div/nav/div/div/div[2]/div/div/div/div/div/div/div[5]/div'
SKIN_PATTERN_XPATH = '/html/body/div/div/div/div/div/div/ul'
SKIN_EXIT_VIEW_IN_3D_XPATH = '/html/body/div/div/div/mat-dialog-container/' \
                             'div/div/app-custom-component/app-modal-wrap/div/button'
SKIN_ITEMS_TYPE_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info' \
                        '/div/div/div/app-related-items/div/app-related-chose-items/div/div'
SKIN_ITEMS_LINK = '/html/body/app-root/div/app-main-site/div/' \
                  'app-full-inventory-info/div/div/div/app-related-items/div/div/div'
SKIN_PRICE_ERROR_XPATH = '/html/body/app-root/div/app-main-site/' \
                         'div/app-full-inventory-info/div/app-page-inventory-info-wrap/div/app-item-failed-status/div'

FAST_SKIN_PATTERN_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/' \
                          'div/app-page-inventory-info-wrap/div/app-full-item-info/div/div[3]/div[3]/div'
FAST_SKIN_FLOAT_XPATH = '/html/body/app-root/div/app-main-site/div/app-full-inventory-info/div/' \
                        'app-page-inventory-info-wrap/div/app-full-item-info/div/div[4]/div[2]'


class BaseDriver(uc.Chrome):
    def __init__(self) -> None:
        chrome_options = uc.ChromeOptions()
        chrome_options.headless = True

        super().__init__(options=chrome_options)
        self.set_window_size(1920, 1080)

        self.skins_data = []
        self.items_data = []

        self.items_link = []
        self.fast_items_link = []

    def driver_sleep(self, time: int, xpath: str) -> bool:
        try:
            wait = WebDriverWait(self, time)
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
