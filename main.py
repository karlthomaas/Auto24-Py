from openpyxl import Workbook
from Bs4 import WebScrape
wb = Workbook()
ws = wb.active
ws.title = 'Vehicles'
print('Excel file has been created!')

link = 'https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=989&f2=2017&f1=2007&ssid=13586566'
webscraping = WebScrape(link)
webscraping.results()
webscraping.main_results()

result_dictionay = webscraping.get_dict()

headings = ['car0'] + list(result_dictionay['car1'].keys()) + ['soodushind']

ws.append(headings)

for vehicle in result_dictionay:
    values = list(result_dictionay[vehicle].values())
    ws.append([vehicle] + values)

wb.save('Auto-24-Py.xlsx')
print('Excel file has been saved and is ready to use!')
