import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import seaborn as sns
sns.set()

# Set start and end dates
start_date = '1994-01-01'
end_date = '2023-01-01'

try:
    # Download data from FRED
    print("Downloading data...")
    gdp_jpn = web.DataReader('JPNRGDPEXP', 'fred', start_date, end_date)
    gdp_usa = web.DataReader('GDPC1', 'fred', start_date, end_date)
    
    # Take natural logarithm of GDP data
    log_gdp_jpn = np.log(gdp_jpn)
    log_gdp_usa = np.log(gdp_usa)
    
    # Apply Hodrick-Prescott filter
    print("Applying HP filter...")
    cycle_jpn, trend_jpn = sm.tsa.filters.hpfilter(log_gdp_jpn, lamb=1600)
    cycle_usa, trend_usa = sm.tsa.filters.hpfilter(log_gdp_usa, lamb=1600)
    
    # Calculate standard deviation of cyclical components
    std_jpn = np.std(cycle_jpn)
    std_usa = np.std(cycle_usa)
    
    # Calculate correlation coefficient of cyclical components
    common_index = cycle_jpn.index.intersection(cycle_usa.index)
    corr = np.corrcoef(cycle_jpn.loc[common_index], cycle_usa.loc[common_index])[0, 1]
    
    # Display results
    print(f"Standard deviation of cyclical component for Japan: {std_jpn:.4f}")
    print(f"Standard deviation of cyclical component for USA: {std_usa:.4f}")
    print(f"Correlation coefficient of cyclical components between Japan and USA: {corr:.4f}")
    
    # Plot graphs
    plt.figure(figsize=(12, 6))
    plt.plot(cycle_jpn, label='Japan')
    plt.plot(cycle_usa, label='USA')
    plt.title('Time Series of Cyclical Components')
    plt.xlabel('Year')
    plt.ylabel('Cyclical Component')
    plt.legend()
    plt.grid(True)
    plt.savefig('cyclical_components.png')
    plt.show()
    plt.close()

except Exception as e:
    print(f"An error occurred: {e}")

print("Program finished.")
