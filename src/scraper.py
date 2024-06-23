from bs4 import BeautifulSoup
import requests


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        webpage = requests.get(self.url)
        return BeautifulSoup(webpage.text, 'html.parser')

    def get_attributes(self, links):
        return [link[link.rfind('/')+1:] for link in links]

    def get_uniques(self, links):
        l = []
        for link in links:
            if link not in l:
                l.append(link)
        return l
    
    def get_links(self):
        top = [link['href'] for link in self.soup.select('a.topStatsLink')]
        more = [link['href'] for link in self.soup.select('nav.moreStatsMenu a')]
        return self.get_uniques(self.get_attributes(more) + self.get_attributes(top))

