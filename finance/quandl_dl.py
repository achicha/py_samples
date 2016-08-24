import Quandl
from pandas import DataFrame, read_csv, ExcelWriter

#search for dataset
def quandl_search(search_element):

    datasets = Quandl.search(query = search_element, page = 2)
    return datasets

def get_quotes_quandl(symbol, start_date, end_date):

    print('downloading data for %s' % (symbol))
    data = Quandl.get(symbol, authtoken='6hgNxKv-HCEFx12yzu3u', trim_start=start_date,
                    trim_end=end_date, collapse='daily', returns='pandas') # returns = "numpy" or "pandas"
    print(data.head(n=3))

def save_to_excel(dataset):

    url = '{0}.xlsx'.format(symbol.replace("/", "."))
    with ExcelWriter(url) as writer:
        dataset.to_excel(writer, 'sheet1')
        #quote.to_excel(writer, 'Data 1')     #write to the second list
        print('saved to file '+url)


if __name__ == "__main__":
    symbol = 'BAVERAGE/USD_BITSTAMP'
    start_date ='2015-01-27'
    end_date = '2015-02-18'
    #get_quotes_quandl(symbol, start_date, end_date)

    quandl_search("OIL")



