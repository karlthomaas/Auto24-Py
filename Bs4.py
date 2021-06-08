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


obj = WebScrape('https://www.auto24.ee/kasutatud/nimekiri.php?b=2&ae=2&bw=149&f2=2009&f1=2002&ssid=13532063')

