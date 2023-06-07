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
