import pandas as pd

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
