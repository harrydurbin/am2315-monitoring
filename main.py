#!/usr/bin/python3
import readam2315
import weather_scraper
import os
import datetime
import time
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
import urllib.request
import json
import sqlite3
import pandas as pd
import config

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "data", "am2315_readings.db")

#sql db config
conn = sqlite3.connect(DATA_PATH)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS am2315readings
		(num INTEGER AUTOINCREMENT, date text, itemp real, ihum real, sjtemp real, sjfeel real)''')

prediction = 0


username = 'harry.durbin'
api_key = config.api_key
py.sign_in(username, api_key)


# def execute()
#     read-am2315.get_readings()

if __name__ == "__main__":


#while True:
	sensor_readings = read-am2315.get_readings()
	sensor_temp = round(sensor_readings[1],2)
	sensor_hum = round(sensor_readings[2],2)
#	outside_temp = round(get_outside_temp(),1)
	cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    weather_scraper.Weather()
    print (weather_scraper.Weather.df)
    sjtempdf = weather_scraper.Weather.df
    sjtempdf = sjtempdf.T
    sjtempreal = sjtempdf[1][2]
    sjtempfeel = 0
    sjtempreal = int(sjtempreal[:len(sjtempreal)-1])

	# Insert a row of data
	conn = sqlite3.connect(DATA_PATH)
	c = conn.cursor()
	new_row = [(cur_time, sensor_temp, sensor_hum, sjtemp, sjtempfeel)]
	c.executemany("INSERT INTO am2315readings ('date', 'itemp', 'ihum', 'sjtemp', 'sjfeel') VALUES (?,?,?,?,?)", new_row)
	conn.commit()

	# if prediction > 0:
	# 	# print (prediction)
	# 	new_row = [(prediction,)]
	# 	c.executemany("INSERT INTO am2315readings ('forecast') VALUES (?)", new_row)
	# 	conn.commit()

	# fetch the recent readings
	df = pd.read_sql_query(
	"""
	SELECT *
	FROM (
	SELECT *
	FROM am2315readings
	ORDER BY date DESC
	LIMIT 24*7
	)
	AS X
	ORDER BY date ASC;
	"""
	, con = conn)

	df['date1'] = pd.to_datetime(df['date']).values
	df['day'] = df['date1'].dt.date
	df['time'] = df['date1'].dt.time
	df.index = df.date1
	df.index = pd.DatetimeIndex(df.index)

    #df = df.drop('forecast',1)
	#df['upper'] = df['outside']
	#df['lower'] = df['outside']

	#model = ARIMA(df['outside'], order=(5,1,0))
	#model_fit = model.fit(disp=0)
	#forecast = model_fit.forecast(5)
	#prediction = round(forecast[0][0],2)
	#t0 = df['date1'][-1]
	#new_dates = [t0+datetime.timedelta(minutes = 60*i) for i in range(1,6)]
	#new_dates1 = map(lambda x: x.strftime('%Y-%m-%d %H:%M'), new_dates)
	#df2 = pd.DataFrame(columns=['date','inside','outside','forecast'])
	#df2.date = new_dates1
	#df2.forecast = forecast[0]
	#df2['upper'] = forecast[0]+forecast[1] #std error
	#df2['lower'] = forecast[0]-forecast[1] #std error
	## df2['upper'] = forecast[2][:,1] #95% confidence interval
	## df2['lower'] = forecast[2][:,0] #95% confidence interval
	#df = df.append(df2)
	#df = df.reset_index()
	recentreadings = df
	#recentreadings['forecast'][-6:-5] = recentreadings['outside'][-6:-5]

	## plot the recent readings

	X=[str(i) for i in recentreadings['date'].values]
	X_rev = X[::-1]
	#y_upper = [j for j in recentreadings['upper']]
	#y_lower = [j for j in recentreadings['lower']]
	#y_lower = y_lower[::-1]

	trace1 = go.Scatter(
	x = X,
	y = [j for j in recentreadings['itemp'].values],
	    name = 'Indoor Temperature',
	    line = dict(
	    color = ('rgb(22, 96, 167)'),
	    width = 4)
	)

	trace2 = go.Scatter(
	x=X,
	y=[j for j in recentreadings['ihum'].values],
	    name = 'Indoor Humidity',
	    line = dict(
	    color = ('rgb(205, 12, 24)'),
	    width = 4)
	)

	#trace3 = go.Scatter(
	#x=X,
	#y=[j for j in recentreadings['forecast'].values],
	#    name = 'ARIMA Forecasted Temperature',
	#    line = dict(
	#    color = ('rgb(205, 12, 24)'),
	#    width = 4,
	#    dash = 'dot')
	#)

	#trace4 = go.Scatter(
	#x = X+X_rev,
	#y = y_upper+y_lower,
	#    fill='tozerox',
	#    fillcolor='rgba(231,107,243,0.2)',
	#    line=go.Line(color='transparent'),
	#    showlegend=True,
	#    name='Std Error'
	#)

	data = [trace1] #, trace2] #, trace3, trace4]

	layout = go.Layout(
	title='Temperature',
	yaxis = dict(title = 'Temp [deg F]')
	)

	fig = go.Figure(data=data, layout=layout)

	plot_url = py.plot(fig, filename='sj_temperature', auto_open = False)



	data2 = [trace2]
	layout2 = go.Layout(
	title = 'Humidity',
	yaxis = dict(title = 'Rel. Humidity [%}')
	)
	fig2 = go.Figure(data = data2, layout=layout2)
	plot_url2 = py.plot(fig2, filename='sj_humidity',auto_open = False)
