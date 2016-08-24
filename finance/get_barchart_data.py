#!/bin/env python

import requests, json
import pandas as pd
import argparse
from datetime import datetime

"""
todo https://en.wiki2.org/wiki/Percent-encoding+Milds for symbols
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Download data from Barchart")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("symbol", type=str, help="Barchart Symbol = SIY00")
    parser.add_argument("start", type=int, help="Start Date = 20160410")
    parser.add_argument("end", type=int, help="End Date = 20160420")
    
    args = parser.parse_args()
    return args

def create_links(_args):
    base =  'http://jscharts-e-barchart.aws.barchart.com//charts/update_dynamic_zoom?callback=Request.JSONP.request_map.request_1&data_time=daily&symbol={}&end={}&start={}&cookie_index=0'
    symbol = _args.symbol
    end = int(datetime.timestamp(datetime.strptime(str(_args.end)+'050000', '%Y%m%d%H%M%S'))*1000)
    start = int(datetime.timestamp(datetime.strptime(str(_args.start)+'050000', '%Y%m%d%H%M%S'))*1000)
    
    link = base.format(symbol, end, start) 
    return link

def parse_data(_link):
    # parse data
    raw_data = requests.get(_link)
    data = json.loads(raw_data.text[36:-1])
    return data

def create_df(_data):  
    # create series
    data = _data
    how_many_columns = len(data['data']['series'])
    
    # create dataframes
    ohlc = data['data']['series'][0]
    ohlc_df = pd.DataFrame(ohlc['data'], columns=['Date','Open', 'High', 'Low', 'Close'])
    
    if how_many_columns>1:
        try:
            volume = data['data']['series'][1]
            volume_df = pd.DataFrame(volume['data']).rename(columns={"x": "Date", "y": "Volume"})
            del volume_df['color']
            result = pd.merge(ohlc_df, volume_df, left_on='Date', right_on='Date', how='outer')
            print("Volume exist")
        except:
            pass
        
    if how_many_columns>2:
        try:
            open_interest = data['data']['series'][2]
            open_interest_df = pd.DataFrame(open_interest['data'], columns=['Date', 'Open_interest'])
            result = pd.merge(result, open_interest_df, left_on='Date', right_on='Date', how='outer')
            print("OI exist")
        except:
            pass
        
    return result

def transform_to_DF_format(_data):
    """to DF date format"""
    result_with_dfdate = []
    for time in _data:
            t = datetime.fromtimestamp(int(time)/1000).strftime('%Y%m%d%H%M%S')
            result_with_dfdate.append(t)
    return result_with_dfdate


def save_data_to_excel(_dataframe, _ISIN):
    with open('{}.csv'.format(_ISIN), "a") as f:
        try:
            _dataframe.to_csv(f, header=True)
        except Exception as e:
            print(e)
    print('saved to {}'.format(_ISIN))


if __name__ == "__main__":
    #link = 'http://jscharts-e-barchart.aws.barchart.com//charts/update_dynamic_zoom?callback=Request.JSONP.request_map.request_1&data_time=daily&symbol=SIY00&end=1461042000000&start=1451595600000&cookie_index=0'
    args = parse_args()
    link = create_links(args)
    data = parse_data(link)
    df = create_df(data)
    DF_date = transform_to_DF_format(df["Date"])
    #add new column to our data_set
    df['DF_Date'] = DF_date
    
    save_data_to_excel(df,args.symbol)