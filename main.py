from driver import Driver, Data
from config import PATH


def get_link(file_name: str) -> list:
    with open(file_name, 'r') as file:
        file_data = file.read()

    return ['https://market.csgo' + link for link in ''.join(file_data.split('\n')).split('https://market.csgo')][1:]


def main():
    driver = Driver()

    while True:
        username = 'something123445'
        password = '35chx8u3F9gK6dd'

        if driver.log_in(username, password):
            break
        else:
            print('Вы не правильно вели логин или пароль')

    print('Вход был успешным')

    driver.parsing_skins(get_link(PATH / 'data.txt'))

    file_data = Data(PATH / 'data.xlsx')
    file_data.save_skin(driver.skins_data)
    file_data.save_items(driver.items_data)
    file_data.save()


if __name__ == '__main__':
    main()
