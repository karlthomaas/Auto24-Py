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
                # car_model = c_d.find(class_='model').get_text()
                # car_engine =c_d.find(class_='engine').get_text()
                car_page = f"https://www.auto24.ee/{c_d.find('a').get('href')}"

                # 6 ->
                if c_d:
                    i += 1
                # 7  ->
                self.cars_dict[f'car{i}'] = {}
                self.cars_dict[f'car{i}']['name'] = car_name
                # self.cars_dict[f'car{i}']['model'] = car_model
                # self.cars_dict[f'car{i}']['engine'] = car_engine
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

    def get_dict(self):
        return self.cars_dict

obj = WebScrape('https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=301&f2=1991&f1=1987&ssid=13529292')
obj.results()
obj.main_results()