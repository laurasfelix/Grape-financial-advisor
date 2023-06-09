import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import csv
from datetime import datetime
import finnhub
import json
  

finnhub_client = finnhub.Client(api_key="chobfq1r01qmdnlqj6t0chobfq1r01qmdnlqj6tg")

def stock_info(stock_name1, stock_name2, stock_name3, stock_name4, stock_name5):
    stock_1 = finnhub_client.stock_candles(stock_name1, 'D', 	1654797309, 1686333309)
    stock_2 = finnhub_client.stock_candles(stock_name2, 'D', 	1654797309, 1686333309)
    stock_3 = finnhub_client.stock_candles(stock_name3, 'D', 	1654797309, 1686333309)
    stock_4 = finnhub_client.stock_candles(stock_name4, 'D', 	1654797309, 1686333309)
    stock_5 = finnhub_client.stock_candles(stock_name5, 'D', 	1654797309, 1686333309)

    date = ['date']

    real_time = []
    
    unix_dates = stock_1['t']
    for i in unix_dates:
        ts = int(i)
        pip = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        real_time.append(pip)

    date = date + real_time

    stock_1['c'] =[ float(x) for x in stock_1['c']]
    stock_2['c'] =[ float(x) for x in stock_2['c']]
    stock_3['c'] =[ float(x) for x in stock_3['c']]
    stock_4['c'] =[ float(x) for x in stock_4['c']]
    stock_5['c'] =[ float(x) for x in stock_5['c']]

    stock_price1 = [stock_name1] + stock_1['c']
    stock_price2 = [stock_name2] + stock_2['c']
    stock_price3 = [stock_name3] + stock_3['c']
    stock_price4 = [stock_name4] + stock_4['c']
    stock_price5 = [stock_name5] + stock_5['c']

    final_list = zip(date,stock_price1, stock_price2, stock_price3, stock_price4, stock_price5)

    with open('custom_bundle.csv', 'w', ) as myfile:
        wr = csv.writer(myfile)
        for word in final_list:
            wr.writerow(word)

    # Read in price data
    df = pd.read_csv("custom_bundle.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights_custom.txt")
    return ef.portfolio_performance(verbose=False)

def read():
    with open("weights_custom.txt", "r") as f:
        data = f.read()
    list_names = []
    list_weights = []
    data = data.replace("\'", "\"")
    js = json.loads(data)
    

    list_names = list(js.keys())
    list_weights = list(js.values())
    list_weights = [float(x) for x in list_weights]
    
    return list_names, list_weights

def opt_quick():
    df = pd.read_csv("custom_bundle.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    return ef.portfolio_performance(verbose=False)
