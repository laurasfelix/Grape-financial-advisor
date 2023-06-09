import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def bundle_opt(bundle_number):

    # Read in price data
    df = pd.read_csv("files/bundle"+ str(bundle_number)+ " - Sheet1.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    return ef.portfolio_performance(verbose=False)

# Assuming there is a dictionary of names/current accounts (key) which stores 
# info about the client, espeicailly their ccurent networth (value)

def net_worth(dictionary_user_name, bundle_number):
    # Read in price data
    df = pd.read_csv("files/bundle"+ str(bundle_number)+ " - Sheet1.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    return mu

def bundle_etf():

    # Read in price data
    df = pd.read_csv("files/bundle"+ str(1)+'etf' + " - Sheet1.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    weights = ef.max_sharpe()
    # cleaned_weights = ef.clean_weights()
    # ef.save_weights_to_file("weights4.txt")
    return ef.portfolio_performance(verbose=False)

