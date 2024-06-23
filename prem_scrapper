import os
import json
import requests
import progressbar
import pandas as pd
from bs4 import BeautifulSoup

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


class StatsFetcher:
    def __init__(self, dates, links):
        self.dates = dates
        self.links = links
        self.api_base = 'https://footballapi.pulselive.com/football/stats/ranked/teams/'

    def fetch_stats(self):
        for date in self.dates.keys():
            df = pd.DataFrame()
            bar = progressbar.ProgressBar(maxval=len(self.links), widgets=[date + '\t', progressbar.Bar('-', '[', ']'), ' ', progressbar.Percentage()])
            bar.start()
            for i, attribute in zip(range(len(self.links)), self.links):
                api = self.api_base + attribute
                headers = {'Origin': 'https://www.premierleague.com'}
                params = {'page': '0', 'pageSize': '20', 'compSeasons': self.dates[date], 'comps': '1', 'altIds': 'true'}
                response = requests.get(api, params=params, headers=headers)
                data = json.loads(response.text)
                teams = [team['owner']['name'] for team in data['stats']['content']]
                values = [team['value'] for team in data['stats']['content']]
                series = pd.Series(values, index=teams, name=attribute)
                df = df.join(series, how='outer') if not df.empty else pd.DataFrame(series)
                bar.update(i + 1)
            bar.finish()
            df.dropna(axis=1, how='all', inplace=True)
            df.fillna(0, inplace=True)
            df.to_csv(f'files/stats/{date}.csv')


class ResultsFetcher:
    def __init__(self, dates):
        self.dates = dates
        self.api_base = 'https://footballapi.pulselive.com/football/fixtures'

    def get_team_ids(self, date):
        api = f'https://footballapi.pulselive.com/football/compseasons/{self.dates[date]}/teams'
        headers = {'Origin': 'https://www.premierleague.com'}
        response = requests.get(api, headers=headers)
        teams = json.loads(response.text)
        team_ids = [team['id'] for team in teams]
        return ','.join(map(str, team_ids))

    def fetch_results(self):
        bar = progressbar.ProgressBar(maxval=len(self.dates), widgets=['', '\t', progressbar.Bar('-', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i, date in zip(range(len(self.dates)), self.dates.keys()):
            bar.widgets[0] = date
            team_ids = self.get_team_ids(date)
            params = {'comps': '1', 'compSeasons': self.dates[date], 'teams': team_ids, 'page': '0', 'pageSize': '380', 'sort': 'asc', 'statuses': 'C', 'altIds': 'true'}
            headers = {'Origin': 'https://www.premierleague.com'}
            response = requests.get(self.api_base, params=params, headers=headers)
            results = json.loads(response.text)
            df_list = [
                [result['teams'][0]['team']['name'], result['teams'][1]['team']['name'], result['teams'][0]['score'], result['teams'][1]['score'], result['outcome']]
                for result in results['content']
            ]
            df = pd.DataFrame(df_list, columns=['home_team', 'away_team', 'home_goals', 'away_goals', 'result'])
            df.to_csv(f'files/results/{date}.csv')
            bar.update(i + 1)
        bar.finish()


class DataValidator:
    def __init__(self, dates):
        self.dates = dates

    def validate_datasets(self):
        datasets = [pd.read_csv(f'files/stats/{date}.csv', index_col=0) for date in self.dates.keys()]
        mismatches = [(i, j) for i in range(4, 12) for j in range(i + 1, 12) if datasets[i].columns.tolist() != datasets[j].columns.tolist()]
        if not mismatches:
            print('Valid Set')
        else:
            print('Invalid Set')


class DataMerger:
    def __init__(self, files):
        self.files = files

    def merge_data(self):
        stats_df = pd.DataFrame()
        results_df = pd.DataFrame()
        for name in self.files:
            # Stats
            stats_series = pd.Series([name[:-4]] * 20, name='season')
            stats_season = pd.concat([pd.read_csv(f'files/stats/{name}', index_col=False), stats_series], axis=1)
            stats_season.columns = ['team'] + stats_season.columns.tolist()[1:]
            stats_df = pd.concat([stats_df, stats_season]) if not stats_df.empty else stats_season
            
            # Results
            results_series = pd.Series([name[:-4]] * 380, name='season')
            results_season = pd.concat([pd.read_csv(f'files/results/{name}'), results_series], axis=1)
            results_df = pd.concat([results_df, results_season]) if not results_df.empty else results_season

        stats_df.to_csv('files/stats/stats.csv', index=False)
        results_df.drop(results_df.columns[0], axis=1, inplace=True)
        results_df.to_csv('files/results/results.csv', index=False)


def main():
    # Ensure necessary directories exist
    if not os.path.exists('files'):
        os.makedirs('files/stats')
        os.makedirs('files/results')

    # Define URLs and dates
    url = 'https://www.premierleague.com/stats/top/clubs/wins?se=578'
    dates = {'2006-2007':15, '2007-2008':16, '2008-2009':17, '2009-2010':18, 
             '2010-2011':19, '2011-2012':20, '2012-2013':21, '2013-2014':22, 
             '2014-2015':27, '2015-2016':42, '2016-2017':54, '2017-2018':79,
             '2018-2019':210, '2019-2020':274, '2020-2021':363, '2021-2022':418,
             '2022-2023':489, '2023-2024':578}
    files = ['2006-2007.csv', '2007-2008.csv', '2008-2009.csv', '2009-2010.csv', '2010-2011.csv', '2011-2012.csv', '2012-2013.csv', '2013-2014.csv', '2014-2015.csv', '2015-2016.csv', '2016-2017.csv', '2017-2018.csv']

    # Scrape web data
    scraper = WebScraper(url)
    links = scraper.get_links()

    # Fetch stats
    stats_fetcher = StatsFetcher(dates, links)
    stats_fetcher.fetch_stats()

    # Fetch results
    results_fetcher = ResultsFetcher(dates)
    results_fetcher.fetch_results()

    # Validate data
    validator = DataValidator(dates)
    validator.validate_datasets()

    # Merge data
    merger = DataMerger(files)
    merger.merge_data()

'''if __name__ == '__main__':
    main()'''
