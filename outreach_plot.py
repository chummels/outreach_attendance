#!/usr/bin/env python

import matplotlib, datetime, matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np

# grab data from outreach_dates file and stick into arrays
# format of text file has columns: month day year number(attendees) clear(bool)
data = np.genfromtxt('caltech.txt',dtype="int32")
month = data[:,0]
day = data[:,1]
year = data[:,2]
number = data[:,3]
clear = data[:,4]

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
	tempdate = datetime.date(year[i],month[i],day[i])
	newdate =  matplotlib.dates.date2num(tempdate)
	if (clear[i] == 0):
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

start = datetime.date(2016, 01, 01)
end = datetime.date(2016, 12, 31)
startnum = matplotlib.dates.date2num(start)
endnum = matplotlib.dates.date2num(end)

# plot clear nights in blue, cloudy nights in red
if len(cleardates) > 0:
    plt.plot_date(cleardates,clearnum,'bo',label='Lecture/Stargazing, Clear Weather')
if len(cloudydates) > 0:
    plt.plot_date(cloudydates,cloudynum,'ro',label='Lecture/Stargazing, Cloudy Weather')
if len(otherdates) > 0:
    plt.plot_date(otherdates,othernum,'go',label='Astronomy on Tap')
plt.legend(loc=2, numpoints=1)
plt.xlabel('Date')
plt.ylabel('Number of Attendees')
plt.title('Caltech Astronomy Outreach Event Attendance')
#increment = (dates[-1]-dates[0])/4.0
#xticklist = np.arange(dates[0],dates[-1],increment-0.1)
#plt.xticks( xticklist )
#plt.axis([dates[0],dates[-1],0,200])		# reset the axes to max at 200
increment = ((endnum-startnum)/4.)
xticklist = np.arange(startnum, endnum, increment-0.1)
plt.xticks( xticklist )
plt.axis([startnum, endnum, 0, 200])		        

plt.savefig('caltech.jpg')
