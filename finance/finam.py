from pandas import DataFrame, read_csv
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from datetime import datetime, timedelta, date
from pandas import DataFrame, read_csv, ExcelWriter
import sys
import numpy as np

finam_symbols = urlopen('http://www.finam.ru/cache/icharts/icharts.js').readlines()
periods = {'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5,
           '30min': 6, 'hour': 7, 'daily': 8, 'week': 9, 'month': 10}

__all__ = ['periods', 'get_quotes_finam']


def __get_finam_code__(symbol):
    s_id = str(finam_symbols[0])
    s_code = str(finam_symbols[2])
    star = str(s_code).find("[\'") + 2
    en = s_code.find("\']")
    names = s_code[star : en].split('\',\'')
    ids = s_id[s_id.find('[') + 1 : s_id.find(']')].split(',')
    if symbol in names:
        max_id = 0
        for i, name in enumerate(names):
            if name == symbol and i > max_id:
                max_id = i
        return int(ids[max_id])
    else:
        raise Exception("%s not found\r\n" % symbol)


def __get_url__(symbol, period, start_date, end_date):
    finam_HOST = "195.128.78.52"
    #'http://195.128.78.52/table.csv?market=1&em=3&code=SBER&df=9&mf=11&yf=2013&dt=9&mt=11&yt=2013&p=1&f=table&e=.csv&cn=SBER&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&datf=9&at=1'
    #'http://195.128.78.52/table.csv?d=d&market=1&f=table&e=.csv&dtf=1&tmf=3&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&at=1&em=20509&p=1&mf=10&cn=FEES&mt=10&df=22&dt=22&yt=2013&yf=2013&datf=11'
    #finam_URL = "/table.csv?d=d&market=1&f=table&e=.csv&dtf=1&tmf=1&MSOR=0&sep=1&sep2=1&at=1&"
    finam_URL = "/table.csv?d=d&market=1&f=table&e=.csv&dtf=1&tmf=3&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&at=1&"
    #'/table.csv?d=d&market=1&f=table&e=.csv&dtf=1&tmf=3&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&at=1'
    symb = __get_finam_code__(symbol)
    params = urlencode({"p": period, "em": symb,
                        "df": start_date.day, "mf": start_date.month - 1,
                        "yf": start_date.year,
                        "dt": end_date.day, "mt": end_date.month - 1,
                        "yt": end_date.year, "cn": symbol})

    stock_URL = finam_URL + params
    if period == periods['tick']:
        return "http://" + finam_HOST + stock_URL + '&code='+ symbol + '&datf=11'
    else:
        return "http://" + finam_HOST + stock_URL + '&datf=5'


def __period__(s):
    return periods[s]


def __get_daily_quotes_finam__(symbol, start_date='20070101', end_date=date.today().strftime('%Y%m%d'),
                               period='daily'):
    """
    Return downloaded daily or more prices about symbol from start date to end date
    """
    start_date = datetime.strptime(start_date, "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()
    url = __get_url__(symbol, __period__(period), start_date, end_date)
    pdata = read_csv(url, index_col=0, parse_dates={'index': [0, 1]}, sep=';').sort_index()

    pdata.columns = [i for i in ['Open', 'High', 'Low', 'Close', 'Volume']]
    sLength = len(pdata['Volume'])
    pdata['Symbol'] = symbol #np.random.randn(sLength)
    return pdata


def __get_quotes_finam__(symbol, start_date='20070101', end_date=date.today().strftime("%Y%m%d"),
                     period='daily'):
    """
    Return downloaded prices for symbol from start date to end date with default period daily
    Date format = YYYYMMDD
    Period can be in ['tick','min','5min','10min','15min','30min','hour','daily','week','month']
    """
    if __period__(period) == periods['tick']:
        return __get_tick_quotes_finam__(symbol, start_date, end_date)
    elif __period__(period) >= periods['daily']:
        return __get_daily_quotes_finam__(symbol, start_date, end_date, period)
    else:
        start_date = datetime.strptime(start_date, "%Y%m%d").date()
        end_date = datetime.strptime(end_date, "%Y%m%d").date()
        url = __get_url__(symbol, __period__(period), start_date, end_date)
        pdata = read_csv(url, index_col=0, parse_dates={'index': [0, 1]}, sep=';').sort_index()
        pdata.columns = [symbol + '.' + i for i in ['Open', 'High', 'Low', 'Close', 'Vol']]
        return pdata


def __get_tick_quotes_finam__(symbol, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()
    delta = end_date - start_date
    data = DataFrame()
    for i in range(delta.days + 1):
        day = timedelta(i)
        url = __get_url__(symbol, periods['tick'], start_date + day, start_date + day)
        req = Request(url)
        req.add_header('Referer', 'http://www.finam.ru/analysis/profile0000300007/default.asp')
        r = urlopen(req)
        try:
            tmp_data = read_csv(r, index_col=0, parse_dates={'index': [0, 1]}, sep=';').sort_index()
            if data.empty:
                data = tmp_data
            else:
                data = data.append(tmp_data)
        except Exception:
            print('error on data downloading {} {}'.format(symbol, start_date + day))

    data.columns = [symbol + '.' + i for i in ['Last', 'Vol', 'Id']]
    return data


def __get_tick_quotes_finam_all__(symbol, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y%m%d").date()
    end_date = datetime.strptime(end_date, "%Y%m%d").date()
    url = __get_url__(symbol, periods['tick'], start_date, end_date)
    req = Request(url)
    req.add_header('Referer', 'http://www.finam.ru/analysis/profile0000300007/default.asp')
    r = urlopen(req)
    pdata = read_csv(r, index_col=0, parse_dates={'index': [0, 1]}, sep=';').sort_index()
    pdata.columns = [symbol + '.' + i for i in ['Last', 'Vol', 'Id']]
    return pdata


def __save_data__(clean_code, startdata, enddata, periodvalue):
    clean_code = clean_code.replace(" ", "").split(',')
    code_lst = []
    for i in clean_code:
        if len(i) > 2:
            code_lst.append(i)

    for y in code_lst:
        try:
            print('download %s data for %s' % (per, y))
            quote = __get_quotes_finam__(y, start_date=startdata, end_date=enddata, period=periodvalue)
            print(quote.head(n=3))
        except:
            print("ошибка скачивания:", sys.exc_info()[0])

        #C:\\Users\\login\\PycharmProjects\\trade\\
        url = '{0}.xlsx'.format(y+"_"+startdata+"_"+enddata)
        try:
            with ExcelWriter(url) as writer:
                quote.to_excel(writer, y)
                #quote.to_excel(writer, 'Data 1')     #write to the second list
                print(y + ' saved to file')
        except:
            print("ошибка записи в файл:", sys.exc_info()[0])


def __get_all_data__(codelst):
    url = '{0}.xlsx'.format(date.today().strftime("%Y%m%d"))
    _df = DataFrame(np.random.randn(1, 6), columns=['Open', 'High', 'Low', 'Close', 'Volume', 'Symbol'])
    #print(_df)

    for y in codelst:
        try:
            #print('download %s data for %s' % ('daily', y))
            quote = __get_quotes_finam__(y, start_date='20150406', end_date='20150406', period='daily')
            #print(quote)
            _df = _df.append(quote[:])
            #print(_df)
        except:
            print("нет инструмента: ", sys.exc_info()[0])
            continue
    with ExcelWriter(url) as writer:
        try:
            _df.to_excel(writer)
            print("Готово")
        except:
            print("ошибка записи в файл:", sys.exc_info()[0])



if __name__ == "__main__":
    code_to_save = 'AFKS, AKRN'
    code_to_all = ['AFKS', 'AKRN','ARMD', 'AVAZ']
        #['AFKS', 'AFLT', 'AKRN', 'ALRS', 'AMEZ', 'APTK', 'ARMD', 'AVAZ', 'AVAZP', 'BANE', 'BANEP', 'BLNG', 'BSPB', 'CHMF', 'CHMK', 'DIXY', 'DZRDP', 'ENRU', 'EONR', 'FEES', 'GAZP', 'GCHE', 'GMKN', 'GRAZ', 'GTLC', 'GTPR', 'HALS', 'HYDR', 'IRAO', 'IRGZ', 'IRKT', 'JNOS', 'KBSB', 'KMAZ', 'KMEZ', 'KZOS', 'LKOH', 'LNTA', 'LSNG', 'LSNGP', 'LSRG', 'LVHK', 'MAGN', 'MFGS', 'MFON', 'MGNT', 'MMBM', 'MOEX', 'MRKC', 'MRKU', 'MRKV', 'MRKY', 'MSNG', 'MSRS', 'MSSB', 'MTLR', 'MTLRP', 'MTSS', 'MVID', 'NLMK', 'NMTP', 'NVNG', 'NVNGP', 'NVTK', 'ODVA', 'OFCB', 'OGKB', 'OPIN', 'PHOR', 'PHST', 'PLSM', 'PLZL', 'POLY', 'RASP', 'RBCM', 'RLMN', 'RLMNP', 'RNAV', 'ROSN', 'RSEA', 'RSTI', 'RTKM', 'RTKMP', 'RUAL', 'RUALR', 'RUGR', 'SBER', 'SBERP', 'SELG', 'SIBN', 'SNGS', 'SNGSP', 'STSB', 'STSBP', 'SVAV', 'SYNG', 'TAER', 'TATN', 'TATNP', 'TGKA', 'TGKB', 'TGKD', 'TGKDP', 'TRMK', 'TRNFP', 'TUCH', 'UNAC', 'URKA', 'UTAR', 'VSMO', 'VTBR', 'VTRS', 'VZRZ', 'YNDX']

    start = '20150406'
    end = '20150406' # date.today().strftime("%Y%m%d")
    per = 'daily'

    #__save_data__(code_to_save, start, end, per)
    __get_all_data__(code_to_all)