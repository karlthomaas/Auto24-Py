from bs4 import BeautifulSoup
import requests


class WebScrape:
    def __init__(self, link):
        self.link = link
        result = requests.get(link)
        rc = result.content
        self.soup = BeautifulSoup(rc, features='html.parser')

    def prettify(self):
        print(self.soup.prettify())

    def result_counter(self):
        """ 1. Searches for the result bar
            2. Takes the result bar text
            3. Splits it into a list, improvised how to get a text, because
            accessing it directly wasn't possible
            4. Returns the text by only selecting 0:2 (which are the results)"""
        counter_tag = self.soup.find(class_='current-range')
        tag = counter_tag.span.get_text()
        tag_list = tag.split(' ')
        return ' '.join(tag_list[0:2])

    def results(self):
        results_section = self.soup.find(class_='section search-list')
        # removes the unnecessary tags from the tree
        results_section.find(class_='insearch-offers-wrap').decompose()
        results_section.find(class_='c2z-section').decompose()

        results = results_section.find_all('div')


        for result in results:
            try:
                c_t = result.find(class_='title')
                car_name = c_t.find('span').get_text()
                car_model = c_t.find(class_='model').get_text()
                car_engine =c_t.find(class_='engine').get_text()

                car_page = f"https://www.auto24.ee/{c_t.find('a').get('href')}"
                print(car_page)
                car_dict = {
                    'name': car_name,
                    'model': car_model,
                    'engine': car_engine,
                    'site': car_page
                }
                print(car_dict)
            except AttributeError:
                ...

        # for result in results:
        #     try:
        #         car_description = result.find(class_='description')
        #         print(car_description.find(class_='title').get_text())
        #     except AttributeError:
        #         ...
obj = WebScrape('https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=301&f2=1991&f1=1987&ssid=13529292')
obj.results()
