import pandas as pd

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
