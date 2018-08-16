# -*- coding: utf-8 -*-
"""
\\--------------------------------------//
''--------------------------------------''
''      Lognormal Returns Generator     ''
''--------------------------------------''
//--------------------------------------\\

Gemerates a csv of asset returns following a log-normal distribution

Created on Wed Aug 15, 2018 by psk91
"""
"""
---------------------------------
   Choose parameters for file
---------------------------------
"""
scenarios = 3000
years = 30
period = 4          # time periods per year. Set 4 for quarterly
annualized = False  # provide output as annualized log returns or per-period log returns
drift = 0.10		# annualized drift of log-return
vol = 0.20			# annualized std. deviation of log-return
seed = None			# specify integer seed or use 'None'
"""
---------------------------------
   Code for generating file
---------------------------------
"""
import numpy as np
import pandas as pd
import csv

np.random.seed(seed)
timeperiods = {12 : 'Monthly', 4 : 'Quarterly', 2 : 'Biannual', 1 : 'Annualized'}

if annualized :
	mu = drift
	sigma = vol
else:
	mu = drift / period
	sigma = vol / np.sqrt(period)

samples = years * period  # sets number of columns in datafile 

# Generate random returns - note that np.random.normal uses mean and stdev as parameters, not mean and var
returns  = pd.Dataframe(np.random.normal(mu, sigma, size=(scenarios, samples)), columns=list(range(1,samples+1)))
returns.index += 1  # label scenarios starting from 1

# Write output to csv, with additional summary info at the top of the file

filepath = 'LogN_Returns__' + str(drift*100) + 'drift_' + str(vol*100) + 'vol.csv'

with open(filepath, mode='w', newline='') as csvfile:
	outputwriter = csv.writer(csvfile, delimiter=',')
	
	if seed is not None:
		outputwriter.writerow([scenarios, 'Scenarios', 'with seed', seed])
	else:
		outputwriter.writerow([scenarios, 'Pseudorandom scenarios'])
	
	outputwriter.writerow(['{0:.2%}'.format(drift), 'Annual Drift Rate'])
	outputwriter.writerow(['{0:.1%}'.format(vol), 'Annual Volatility'])
	
	if annualized:
		outputwriter.writerow(['Annualized Data'])
	elif period in timeperiods:
		outputwriter.writerow([timeperiods[period] + 'Data'])
	else:
		outputwriter.writerow([period, 'periods per year'])
	outputwriter.writerow([years, 'years'])
	outputwriter.writerow([])
	
returns.to_csv(filepath, mode='a') # append Dataframe of returns to csv
