from bs4 import BeautifulSoup
import requests


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
                car_model = c_d.find(class_='model').get_text()
                car_engine =c_d.find(class_='engine').get_text()
                car_page = f"https://www.auto24.ee/{c_d.find('a').get('href')}"

                # 6 ->
                if c_d:
                    i += 1
                # 7  ->
                self.cars_dict[f'car{i}'] = {}
                self.cars_dict[f'car{i}']['name'] = car_name
                self.cars_dict[f'car{i}']['model'] = car_model
                self.cars_dict[f'car{i}']['engine'] = car_engine
                self.cars_dict[f'car{i}']['link'] = car_page

            except AttributeError:
                ...

obj = WebScrape('https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=301&f2=1991&f1=1987&ssid=13529292')

