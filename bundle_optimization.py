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
    cleaned_weights = ef.clean_weights()
    ef.save_weights_to_file("weights"+str(bundle_number)+".txt")  # saves to file
    print(cleaned_weights)
    return ef.portfolio_performance(verbose=False)

# Assuming there is a dictionary of names/current accounts (key) which stores 
# info about the client, espeicailly their ccurent networth (value)

def net_worth(dictionary_user_name, bundle_number):
    # Read in price data
    df = pd.read_csv("files/bundle"+ str(bundle_number)+ " - Sheet1.csv", parse_dates=True, index_col="date")

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    if dictionary_user_name['initial_investing_amount'] == 0:
        # net_statement = f"The client, {dictionary_user_name['name']}, is investing for the first time, so their current net worth is {0} and \
        # their annual net worth will be {mu}."

        dictionary_user_name['expected_net_worth'] = mu
        return dictionary_user_name['expected_net_worth']
    else:
        # net_statement = f"The client, {dictionary_user_name['name']}'s, current net worth is \
        # {dictionary_user_name['initial_investing_amount']} and {dictionary_user_name['name']}'s annual net worth will be \
        # {dictionary_user_name['expected_net_worth']+ mu}."


        dictionary_user_name['expected_net_worth'] += mu
        return dictionary_user_name['expected_net_worth']
