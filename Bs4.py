from bs4 import BeautifulSoup
import requests
import unidecode


class WebScrape:
    def __init__(self, link):
        self.link = link
        result = requests.get(link)
        rc = result.content
        self.soup = BeautifulSoup(rc, features='html.parser')
        self.cars_dict = {}

    def prettify(self):
        print(self.soup.prettify())

    def result_counter(self):
        """ 1. Searches for the result bar
            2. Takes the result bar text
            3. Splits it into a list, improvised how to get a text, because
            accessing it directly wasn't possible
            4. Returns the text by only selecting 0:2 (which are the results)"""
        counter_tag = self.soup.find(class_='current-range')  # 1
        tag = counter_tag.span.get_text()  # 2
        tag_list = tag.split(' ')  # 3
        return ' '.join(tag_list[0:2])  # 4

    def results(self):
        """
        1. Takes the results section
        2. Removes unnecessary tags
        3. Takes all the results and puts them into a list
        4. Cycles through the list
        5. Takes the name, model, engine and page link
        6. Check's if the car exists
        7. Stores all the information into a dictionary
        """
        results_section = self.soup.find(class_='section search-list')  # 1
        # removes the unnecessary tags from the tree

        results_section.find(class_='insearch-offers-wrap').decompose()  # 2
        results_section.find(class_='c2z-section').decompose()  # 2

        results = results_section.find_all('div')  # 3

        i = 0
        for result in results:  # 4
            try:

                # 5 ->
                # c_d -> car description
                c_d = result.find(class_='description')
                car_name = c_d.find('span').get_text()
                car_page = f"https://www.auto24.ee/{c_d.find('a').get('href')}"

                # 6 ->
                if c_d:
                    i += 1
                # 7  ->
                self.cars_dict[f'car{i}'] = {}
                self.cars_dict[f'car{i}']['name'] = car_name
                self.cars_dict[f'car{i}']['link'] = car_page

            except AttributeError:
                ...

    def main_results(self):

        """
        Script goes to new site and starts to harvest information from there.
        1. Does a for cycle, in order to get all key values.
        2. takes they car dictionary link and assigns it into result object.
        3. Finds the main-data column.
        4. Starts to get all the details from the for cycle.
        5. Takes the detail text.
        6. Splits it by \n.
        7. Takes the detail key  and removes the ":" behind the str, also converts the str into lower case.
        8. Takes the detail value and assigns it to a variable.
        9. Fixes \xa0 problem.
        10. Adds the details into dictionary.
        """

        for key in self.cars_dict.keys():  # 1
            result = requests.get(self.cars_dict[key]['link'])  # 2
            rc = result.content
            soup = BeautifulSoup(rc, features='html.parser')

            main_data = soup.find(class_='main-data')  # 3
            sektsioonid = main_data.find_all('tr')

            # võtab iga lahtri
            # todo reg. number ja vin.kood on liiga pikad, tuleb kas eemaldada või siis teha lühemaks.
            for sektsioon in sektsioonid:  # 4

                tekst = sektsioon.get_text()  # 5
                tl = tekst.split('\n')  # 6

                # 7 ->
                car_key_old = tl[1]
                car_key = car_key_old[:-1].lower()

                # 8
                car_value = tl[2]
                if car_value:
                    ...
                else:
                    car_value = '-'
                # 9
                car_value = unidecode.unidecode(car_value)

                # 10
                self.cars_dict[key][car_key] = car_value
        print(self.cars_dict)

    def get_dict(self):
        return self.cars_dict

class Webscrape2:
    def __init__(self, link):
        self.link = link
        self.count = 0
        self.i = 0

        # the main dictionary where all data is being stored.
        self.cars_dict = {}

        """
        example dictionary ->
        is a template dictionary and
        also a template for excel first row."""
        self.cars_dict_example = {
            'mark': '-',
            'liik': '-',
            'keretüüp': '-',
            'esmane reg': '-',
            'mootor': '-',
            'kütus': '-',
            'läbisõidumõõdiku näit': '-',
            'vedav sild': '-',
            'käigukast': '-',
            'värvus': '-',
            'hind': '-',
            'soodushind': '-',
            'link': '-',
            'pealkiri': '-'}

    def results(self):
        self.result = requests.get(self.link)
        self.rc = self.result.content
        self.soup = BeautifulSoup(self.rc, features='html.parser')

        results_section = self.soup.find(class_='section search-list')

        try:
            # removes all unnecessary trash.
            results_section.find(class_='insearch-offers-wrap').decompose()
            results_section.find(class_='c2z-section').decompose()

            # when there's no more trash. (usually page one only has!)
        except:
            ...
        # result object ->
        results = results_section.find_all('div')

        """The following for loop is responsible for creating dictionaries for all of the vehicles"""
        self.i += 1
        print(f'Scanning page {self.i}')
        for result in results:  # 4
            try:
                c_d = result.find(class_='description')
                car_name = c_d.find('span').get_text()
                car_page = f"https://www.auto24.ee/{c_d.find('a').get('href')}"
                header = result.find(class_='title').get_text()

                if c_d:
                    self.count += 1
                self.cars_dict[self.count] = {}
                self.cars_dict[self.count] = self.cars_dict_example.copy()
                self.cars_dict[self.count]['pealkiri'] = header
                self.cars_dict[self.count]['mark'] = car_name
                self.cars_dict[self.count]['link'] = car_page

            except AttributeError:
                ...

        try:
            # goes for another round, if there's more!

            next_page_div = self.soup.find(class_='paginator in-footer pc-wide')
            if not next_page_div:
                next_page_div = self.soup.find(class_='paginator in-footer')

            next_page = next_page_div.find(class_="next-page")
            self.link = f"https://www.auto24.ee/{next_page.a.get('href')}"
            self.results()
        except Exception as e:
            ...
    """The following function is responsible for providing 
        the dictionaries with detailed information
        from websites. """
    def main_results(self):
        try:
            print('Gathering information for each car!')
            i = 0
            # cycles through all of the keys
            for key in self.cars_dict.keys():
                i += 1
                print(f'Gathering information about: ({i}/{len(self.cars_dict)}) car! ')
                if key != 0:
                    # get's the vehicle link and scraps it
                    result = requests.get(self.cars_dict[key]['link'])
                    rc = result.content
                    soup = BeautifulSoup(rc, features='html.parser')

                    # main data object ->
                    main_data = soup.find(class_='main-data')
                    sektsioonid = main_data.find_all('tr')

                    # for loops through all of the details
                    for sektsioon in sektsioonid:
                        # get's the details and makes it to a list
                        tekst = sektsioon.get_text()
                        tl = tekst.split('\n')

                        # detail category name obj. ->
                        car_key_old = tl[1]
                        car_key = car_key_old[:-1].lower()

                        # check's if the key is in dictionary (prevents inserting car VIN code and more stuff)
                        if car_key in self.cars_dict_example.keys():
                            car_value = tl[2]
                            # unicodes the value
                            car_value = unidecode.unidecode(car_value)
                            self.cars_dict[key][car_key] = car_value
        except Exception as e:
            # happends in very few cases, when website is differently built! 1/1000 chance!
            print(e)

    def get_dict(self):
        return self.cars_dict

    def get_example_dict(self):
        return self.cars_dict_example
