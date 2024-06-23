from utils.file_utils import create_directories
from src.scraper import WebScraper
from src.fetcher import StatsFetcher, ResultsFetcher
from src.validator import DataValidator
from src.merger import DataMerger


def main():
    # Ensure necessary directories exist
    create_directories()

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


if __name__ == '__main__':
    main()
