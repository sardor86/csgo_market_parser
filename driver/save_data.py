from openpyxl import Workbook


class Data:
    def __init__(self, path: str):
        self.file_name = path
        self.wb = Workbook()

    def save_skin(self, skins_list: dict) -> None:
        for skin_data in skins_list:
            self.wb.create_sheet(skin_data['name'][0:31])
            ws = self.wb[skin_data['name'][0:31]]

            ws['A1'] = 'price'
            ws['B1'] = 'float'
            ws['C1'] = 'pattern'
            ws['D1'] = 'sticker'
            ws['E1'] = 'link'

            ws['A2'] = skin_data['price']
            ws['B2'] = skin_data['float']
            ws['C2'] = skin_data['pattern']
            ws['D2'] = skin_data['stickers']
            ws['E2'] = skin_data['url']

    def save_items(self, items_list: dict) -> None:
        row = 2

        self.wb.create_sheet('all_items')
        ws = self.wb['all_items']

        ws['A1'] = 'Item'
        ws['B1'] = 'price'
        ws['C1'] = 'float'
        ws['D1'] = 'pattern'
        ws['E1'] = 'stickers'
        ws['F1'] = 'link'

        for item_data in items_list:
            ws['A' + str(row)] = item_data['name']
            ws['B' + str(row)] = item_data['price']
            ws['C' + str(row)] = item_data['float']
            ws['D' + str(row)] = item_data['pattern']
            ws['E' + str(row)] = item_data['stickers']
            ws['F' + str(row)] = item_data['url']
            row += 1

    def __del__(self):
        self.wb.save(self.file_name)
