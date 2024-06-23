import json
import requests
import progressbar
import pandas as pd

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
