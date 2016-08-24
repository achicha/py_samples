import requests
from datetime import datetime
from sys import argv
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Download data from Bloomberg")
    parser.add_argument("symbol", type=str, help="Bloomberg symbol = SHCOMP:IND")
    parser.add_argument("--interval", action="store", choices=['intraday','historical'], default='historical' ,help="true if historical, and false if you need instraday data")
    #parser.set_defaults(interval=True)
    #parser.add_argument("start", type=int, help="Start Date = 20160410")
    #parser.add_argument("end", type=int, help="End Date = 20160420")
    
    args = parser.parse_args()
    return args

def create_links(_args):
    links = []
    if _args.interval=='historical':
        links.append('http://www.bloomberg.com/markets/api/bulk-time-series/price/{}?timeFrame=1_YEAR'.format(str(_args.symbol)))
    elif _args.interval=='intraday':
        links.append('http://www.bloomberg.com/markets/chart/data/1D/'+ str(_args.symbol))
    try:
        requests.get(links[0]).json()
    except:
        print(links)
        return "symbol is wrong"
    else:
        return links

def get_Bloomberg_data(_links, _args):
    data = []
    for link in _links:
        r = requests.get(link)
        if _args.interval=='historical':
            dt = [[(datetime.timestamp(datetime.strptime(x['date'], "%Y-%m-%d")))*1000,x['value']] for x in r.json()[0]['price']]
        elif _args.interval=='intraday':
            dt = r.json()['data_values']
        data.append(dt)
    return data

#not used for now
def transform_to_DF_format(_data):
    s = []
    for each_symbol in _data:
        temp_data = []
        for time, close_value in each_symbol:
            t = datetime.fromtimestamp(int(time)/1000).strftime('%Y%m%d%H%M%S')
            temp_data.append((t,close_value))
        s.append(temp_data)
        temp_data = []
    return s
    

if __name__ == "__main__":
    #links for testing
    #links =  ['http://www.bloomberg.com/markets/chart/data/1D/SET50:IND']
    #links = ['http://www.bloomberg.com/markets/api/bulk-time-series/price/SET50%3AIND?timeFrame=MAX']
    
    symbol_args = parse_args()
    print(symbol_args)
    links = create_links(symbol_args)
    print(links)
    if links != "symbol is wrong":
        data = get_Bloomberg_data(links, symbol_args)
        df_data = transform_to_DF_format(data)
        with open("{}.txt".format((symbol_args.symbol).split(':')[0]), "w") as f:
            for raw in df_data[0]:
                f.write(str(raw))
                f.write('\n')

        if symbol_args.interval=='historical':
            print('Historical data')
        elif symbol_args.interval=='intraday':
            print('Intraday data')
        print("Symbol: ", symbol_args.symbol, " Start: ",df_data[0][0], " End: ", df_data[0][-1])