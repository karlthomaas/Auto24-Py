from openpyxl import Workbook
from Bs4 import WebScrape, Webscrape2


def func1():
    """
    First version of this project. Kind of buggy, and sometimes puts the results into wrong columns
    because the site doesn't always provide the same details. For example sometime the fuel type is missing thus
    putting the next detail into the fuel type column.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = 'Vehicles'
    print('Excel file has been created!')

    link = 'https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=814&f2=1992&f1=1988&ssid=13812094'
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

def func2():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Vehicles'
    print('Excel file has been created!')

    link = 'https://www.auto24.ee/kasutatud/nimekiri.php?b=23&ae=2&bw=719&f2=2019&f1=2013&ssid=13843681'
    webscraping = Webscrape2(link)
    webscraping.results()
    webscraping.main_results()

    result_dictionay = webscraping.get_dict()
    headings = [0] + list(webscraping.get_example_dict().keys())

    ws.append(headings)

    for vehicle in result_dictionay:
        values = list(result_dictionay[vehicle].values())
        ws.append([vehicle] + values)
    wb.save('Auto-24-Py.xlsx')
    print('Excel file has been saved and is ready to use!')

func2()
