import pandas as pd
pd.set_option('display.max_columns', None)

# Load data
url = 'https://dataverse.nl/api/access/datafile/354098'
pwt1001 = pd.read_stata(url)

# Filter and select relevant columns and countries
countries = ['Australia', 'Austria', 'Belgium', 'Canada', 'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Iceland', 'Ireland', 'Italy', 'Japan', 'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom', 'United States']
data = pwt1001.loc[pwt1001['country'].isin(countries)][['country', 'countrycode', 'year', 'rgdpna', 'rkna', 'emp', 'avh', 'labsh', 'rtfpna']]
data = data.loc[(data['year'] >= 1970) & (data['year'] <= 2015)].dropna()

# Calculate additional variables
data['alpha'] = 1 - data['labsh']
data['y_n'] = data['rgdpna'] / data['emp']  # Y/N
data['k_n'] = data['rkna'] / data['emp']  # K/N
data['l_n'] = data['emp'] * data['avh']  # L/N
data['tfp_term'] = data['rtfpna'] ** (1 / (1 - data['alpha']))  # A^(1/(1-alpha))

# Calculate growth rates
data = data.sort_values(['countrycode', 'year']).groupby('countrycode').apply(lambda x: x.assign(
    growth_rate=x['y_n'].pct_change() * 100,
    tfp_growth=x['tfp_term'].pct_change() * 100,
    capital_deepening=(x['k_n'] / x['y_n']).pct_change() * x['alpha'] * 100,
    labor_growth=(x['l_n'] / x['y_n']).pct_change() * (1 - x['alpha']) * 100,
    tfp_share=x['tfp_term'].pct_change() / x['y_n'].pct_change(),
    capital_share=(x['k_n'] / x['y_n']).pct_change() * x['alpha'] / x['y_n'].pct_change(),
    labor_share=(x['l_n'] / x['y_n']).pct_change() * (1 - x['alpha']) / x['y_n'].pct_change()
)).reset_index(drop=True).dropna()

# Calculate mean growth rates for each country
results = data.groupby('country')[['growth_rate', 'tfp_growth', 'capital_deepening', 'labor_growth', 'tfp_share', 'capital_share', 'labor_share']].mean().reset_index()

# Print the results with percentages
print(results[['country', 'growth_rate', 'tfp_growth', 'capital_deepening', 'labor_growth']].rename(columns={'growth_rate': 'GDP Growth Rate (%)', 'tfp_growth': 'TFP Growth Rate (%)', 'capital_deepening': 'Capital Deepening (%)', 'labor_growth': 'Labor Growth (%)'}).join(results[['tfp_share', 'capital_share', 'labor_share']].rename(columns={'tfp_share': 'TFP Share', 'capital_share': 'Capital Share', 'labor_share': 'Labor Share'})))
