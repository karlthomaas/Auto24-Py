from openpyxl import Workbook
from Bs4 import WebScrape, Webscrape2


# old version
def scrapper1(link):
    """
    First version of this project. Kind of buggy, and sometimes puts the results into wrong columns
    because the site doesn't always provide the same details. For example sometime the fuel type is missing thus
    putting the next detail into the fuel type column.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = 'Vehicles'
    print('Excel file has been created!')

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


# improved version:
def scrapper2(link):
    """
    Second version of this project. Works flawlessly.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = 'Vehicles'
    print('Excel file has been created!')

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

# example links:
# https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=301&f2=1991&f1=1987&ssid=13712424
# https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=2136&f2=2018&f1=2011&ssid=14029839
# https://www.auto24.ee/kasutatud/nimekiri.php?b=23&ae=2&bw=720&f2=2011&f1=2007&ssid=14030034
# https://www.auto24.ee/kasutatud/nimekiri.php?b=4&ae=2&bw=809&f2=2010&f1=2007&ssid=14030330

link = 'https://www.auto24.ee/kasutatud/nimekiri.php?b=4&ae=2&bw=809&f2=2010&f1=2007&ssid=14030330'
# scrapper1(link)
# scrapper2(link)
