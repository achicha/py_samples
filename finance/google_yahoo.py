import pandas.io.data as web
import datetime
from pandas import ExcelWriter

# http://pandas.pydata.org/pandas-docs/dev/remote_data.html

# dataset = web.DataReader('AAPL', 'goolge', datetime.datetime(2013, 1, 1), datetime.datetime(2015, 1, 27))

def google_and_yahoo_search(symbol, start, end):
    g = web.DataReader(symbol, 'google', start, end)
    print("Google result:")
    print(g.tail(n=5))
    print(g.head(n=5))
    y = web.DataReader(symbol, 'yahoo', start, end)
    print("Yahoo result:")
    print(y.tail(n=5))
    print(y.head(n=5))


def data_download(symbol, source, start, end):
    dataset = web.DataReader(symbol, source, start, end)
    url = '{0}.xlsx'.format(symbol.replace("/", "."))
    with ExcelWriter(url) as writer:
        dataset.to_excel(writer, 'sheet1')
        # quote.to_excel(writer, 'Data 1')     # write to the second list
        print('saved to file '+url)


if __name__ == "__main__":
    symbol = "AAPL"
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2014, 1, 27)
    google_and_yahoo_search(symbol, start, end)

    source = "google"
    data_download(symbol, source, start, end)