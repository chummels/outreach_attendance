#!/usr/bin/env python

import pylab, matplotlib, datetime, matplotlib.dates

# grab data from outreach_dates file and stick into arrays
# format of text file has columns: month day year number(attendees) clear(bool)
data = pylab.load('outreach_dates.txt')
month = data[0:len(data),0]
day = data[0:len(data),1]
year = data[0:len(data),2]
number = data[0:len(data),3]
clear = data[0:len(data),4]

# create empty arrays for plotting against each other
cleardates = []
cloudydates = []
otherdates = []
dates = []
clearnum = []
cloudynum = []
othernum = []

# populate the arrays with appropriate dates and corresponding turnout
for i in range(len(month)):
	tempdate = matplotlib.datetime.date(year[i],month[i],day[i])
	newdate =  matplotlib.dates.date2num(tempdate)
	if (clear[i] == 1):
		cleardates.append(newdate)
		clearnum.append(number[i])
		dates.append(newdate)
	elif (clear[i] == 2):
		otherdates.append(newdate)
		othernum.append(number[i])
		dates.append(newdate)
	else:
		cloudydates.append(newdate)
		cloudynum.append(number[i])
		dates.append(newdate)

# plot clear nights in blue, cloudy nights in red
pylab.plot_date(cleardates,clearnum,'bo',label='Stargazing Clear Nights')
pylab.plot_date(cloudydates,cloudynum,'ro',label='Stargazing Cloudy Nights')
pylab.plot_date(otherdates,othernum,'go',label='Other Events')
pylab.legend(loc=2)
pylab.xlabel('Date')
pylab.ylabel('Number of Attendees')
pylab.title('Attendance at Outreach Lectures and Stargazing Nights')
increment = (dates[-1]-dates[0])/6.0
xticklist = pylab.arange(dates[0],dates[-1],increment-0.1)
pylab.xticks( xticklist )
pylab.axis([dates[0],dates[-1],0,400])		# reset the axes to max at 400

pylab.savefig('outreach_dates.jpg')
pylab.show()
