myHPfilter

import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas_datareader as pdr
import numpy as np

# set the start and end dates for the data
start_date = '1994-01-01'
end_date = '2023-01-01'

# download the data from FRED using pandas_datareader
gdp_jpn = web.DataReader('JPNRGDPEXP', 'fred', start_date, end_date)
gdp_deu = web.DataReader('CLVMNACSCAB1GQDE', 'fred', start_date, end_date)

#take the logarithm of the GDP data
log_gdp_jpn = np.log(gdp_jpn)
log_gdp_gmn = np.log(gdp_deu)

# calculate the quarterly percent change in real GDP
gdp_pct_change_jpn = gdp_jpn.pct_change(4)
gdp_pct_change_deu = gdp_deu.pct_change(4)

# apply a Hodrick-Prescott filter to the data to extract the cyclical component
cycle, trend = sm.tsa.filters.hpfilter(log_gdp, lamb=1600)

# Plot the original time series data
plt.plot(log_gdp, label="Original GDP (in log)")

# Plot the trend component
plt.plot(trend, label="Trend")

# Add a legend and show the plot
plt.legend()
plt.show()
