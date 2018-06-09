#!/usr/bin/python3
from AM2315 import *
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
#from statsmodels.tsa.arima_model import ARIMA

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "data", "am2315_readings.db")

#sql db config
conn = sqlite3.connect(DATA_PATH)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS am2315_readings
		(date text, itemp real, ihum real)''')
prediction = 0


username = 'harry.durbin'
api_key = config.api_key
print (api_key) 
py.sign_in(username, api_key)

def get_readings():
	sensor = AM2315()
	t = datetime.datetime.now()
	temp = sensor.temperature()*9.0/5.0 + 32.0
	hum = sensor.humidity()
	print ('#####################################################')
	print (t)
	print (temp)
	print (hum)
	#print '{} temperature is {} and humidity is {}'.format('Indoor',temp,hum)
	#print 'Time is {}.'.format(t)
	return t,temp, hum

# scrape wunderground api to get outside temperature
#def get_outside_temp():
#  f1 = urllib.request.urlopen('http://api.wunderground.com/api/0f0bb5973a4d0927/conditions/q/CA/Palm_Springs.json')
#  json_string = f1.read()
#  parsed_json = json.loads(json_string)
#  parsed_json.keys()
#  ps_temp_f = parsed_json['current_observation']['temp_f']
#  print ('Outside:', ps_temp_f)
#  f1.close()
#	ps_temp_f = 75
#	return ps_temp_f

if __name__ == "__main__":
#while True:
	sensor_readings = get_readings()
	sensor_temp = round(sensor_readings[1],2)
	sensor_hum = round(sensor_readings[2],2)
#	outside_temp = round(get_outside_temp(),1)
	cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

	# Insert a row of data
	conn = sqlite3.connect(DATA_PATH)
	c = conn.cursor()
	new_row = [(cur_time, sensor_temp, sensor_hum,)]
	c.executemany("INSERT INTO am2315_readings ('date', 'itemp', 'ihum') VALUES (?,?,?)", new_row)
	conn.commit()

	if prediction > 0:
		print (prediction)
		new_row = [(prediction,)]
		c.executemany("INSERT INTO am2315_readings ('forecast') VALUES (?)", new_row)
		conn.commit()

	# fetch the recent readings
	df = pd.read_sql_query(
	"""
	SELECT *
	FROM (
	SELECT *
	FROM am2315_readings
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


#	time.sleep(60*30) # delay between stream posts



#if __name__ == "__main__":
#        while True:
#                get_readings()
#                time.sleep(30)

#usr/bin/python3

#"""
#Script to scrape weather data with selenium
#Harry Durbin

#Notes:
#+ must install browser driver and update path below to allow selenium to run.
#+ initialize an empty database by running init_sunnyportal_table.py in tests folder
#"""

#from pyvirtualdisplay import Display
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#import pandas as pd
#import calendar
#import datetime
#from dateutil import parser

## pyvirtualdisplay settings
#display = Display(visible=0, size=(800, 600))
#display.start()


#class Weather(object):

    ## set variables
    #BASE_URL = 'https://www.accuweather.com/en/us/san-jose-ca/95112/hourly-weather-forecast/39767_pc'

    ## assigning web driver for selenium (download chrome driver and set path below)
    #DRIVER_PATH = '/home/hd/Downloads/geckodriver'

    #def __init__(self):
        #self.DRIVER = self.get_driver()
        #self.execute()

    #def get_driver(self):
        #DRIVER = webdriver.Firefox(executable_path = self.DRIVER_PATH)
        #return DRIVER

    #def go_to_site(self):
        #self.DRIVER.get(self.BASE_URL)

#    def get_temp(self):

        #TEMPTABLE = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'hourly-table.overview-hourly')))
        #temp_html = TEMPTABLE.get_attribute('innerHTML')
        # print (temp_html)
    #     self.power = pd.read_html(power_html, header = 0)
        #df = pd.read_html(temp_html,header=0)[0]
        #df.to_csv('cron_test.csv')
        ## ORIGIN = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Origin"]')))
        ## ORIGIN.send_keys(self.ORIGIN_CITY)
        ## DESTINATION = WebDriverWait(self.DRIVER, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Destination"]')))
        ## DESTINATION.send_keys(self.DESTINATION_CITY)
        #print (df)

    #def execute(self):
        #print ('Accessing site...')
        #self.go_to_site()
        #self.get_temp()


#if __name__ == '__main__':
    #Weather()
    #display.stop()

