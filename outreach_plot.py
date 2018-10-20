#!/usr/bin/env python

import matplotlib, datetime, matplotlib.dates
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker


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
dates = []
aotdates = []
aotnum = []
otherdates = []
othernum = []
guerilladates = []
guerillanum = []
clearnum = []
cloudynum = []

# populate the arrays with appropriate dates and corresponding turnout
for i in range(len(month)):
	tempdate = datetime.date(year[i],month[i],day[i])
	newdate =  matplotlib.dates.date2num(tempdate)
	if (clear[i] == 0):
		cleardates.append(newdate)
		clearnum.append(number[i])
		dates.append(newdate)
	elif (clear[i] == 2):
		aotdates.append(newdate)
		aotnum.append(number[i])
		dates.append(newdate)
	elif (clear[i] == 3):
		otherdates.append(newdate)
		othernum.append(number[i])
		dates.append(newdate)
	elif (clear[i] == 4):
		guerilladates.append(newdate)
		guerillanum.append(number[i])
		dates.append(newdate)
	else:
		cloudydates.append(newdate)
		cloudynum.append(number[i])
		dates.append(newdate)

start = datetime.date(2011, 1, 1)
#start = datetime.date(2013, 1, 1)
end = datetime.date(2018, 1, 1)
end = datetime.date(2018, 10, 20)
switch = datetime.date(2015, 10, 1)
startnum = matplotlib.dates.date2num(start)
endnum = matplotlib.dates.date2num(end)
switchnum = matplotlib.dates.date2num(switch)

# plot clear nights in blue, cloudy nights in red
if len(cleardates) > 0:
    plt.plot_date(cleardates,clearnum,'bo',label='Lecture/Stargazing')
if len(cloudydates) > 0:
    plt.plot_date(cloudydates,cloudynum,'ro',label='Lecture/Stargazing, Cloudy Weather')
if len(aotdates) > 0:
    plt.plot_date(aotdates,aotnum,'go',label='Astronomy on Tap')
if len(guerilladates) > 0:
    plt.plot_date(guerilladates,guerillanum,'yo',label='Guerilla Astro')
if len(otherdates) > 0:
    plt.plot_date(otherdates,othernum,'ro',label='Special Event')
#plt.plot_date([switchnum, switchnum], [0,5000], 'k')#, label='CBH joins Caltech')
plt.legend(loc=2, numpoints=1)
plt.xlabel('Date')
plt.ylabel('Number of Attendees')
plt.title('Caltech Astronomy Outreach Event Attendance')
#increment = (dates[-1]-dates[0])/4.0
#xticklist = np.arange(dates[0],dates[-1],increment-0.1)
#plt.xticks( xticklist )
#plt.axis([dates[0],dates[-1],0,200])		# reset the axes to max at 200
#increment = ((endnum-startnum)/5.)
#xticklist = np.arange(startnum, endnum, increment-0.1)
#plt.xticks( xticklist )
locator = matplotlib.dates.YearLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()
ax = plt.gca()
ax.set_yscale('log')
ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax.text(switchnum, 50, 'CBH joins Caltech', rotation='vertical', horizontalalignment='left', verticalalignment='bottom', fontsize=15)
plt.axis([startnum, endnum, 10, 3000])		        
plt.savefig('caltech_outreach_attendance.pdf')

#import pdb; pdb.set_trace()

# histogram plot
year_range = list(range(start.year, end.year+1))
clear_tot = np.empty(len(year_range))
aot_tot = np.empty(len(year_range))
guerilla_tot = np.empty(len(year_range))
other_tot = np.empty(len(year_range))
clear_num_events = np.empty(len(year_range))
aot_num_events = np.empty(len(year_range))
guerilla_num_events = np.empty(len(year_range))
other_num_events = np.empty(len(year_range))

for i, year in enumerate(year_range):
    count = 0
    count2 = 0
    for j in range(len(cleardates)):
        if matplotlib.dates.num2date(cleardates[j]).year == year:
            count += clearnum[j]
            count2 += 1
    clear_tot[i] = count    
    clear_num_events[i] = count2
    count = 0
    count2 = 0
    for j in range(len(aotdates)):
        if matplotlib.dates.num2date(aotdates[j]).year == year:
            count += aotnum[j]
            count2 += 1
    aot_tot[i] = count    
    aot_num_events[i] = count2
    count = 0
    count2 = 0
    for j in range(len(guerilladates)):
        if matplotlib.dates.num2date(guerilladates[j]).year == year:
            count += guerillanum[j]
            count2 += 1
    guerilla_tot[i] = count    
    guerilla_num_events[i] = count2
    count = 0
    count2 = 0
    for j in range(len(otherdates)):
        if matplotlib.dates.num2date(otherdates[j]).year == year:
            count += othernum[j]
            count2 += 1
    other_tot[i] = count    
    other_num_events[i] = count2

# plot it
fig, ax = plt.subplots(1,1)
p1 = plt.bar(year_range, other_tot, color=u'r', width=.9)
p2 = plt.bar(year_range, guerilla_tot, color=u'y', bottom=other_tot, width=.9)
p3 = plt.bar(year_range, aot_tot, color=u'g', bottom=other_tot+guerilla_tot, width=.9)
p4 = plt.bar(year_range, clear_tot, color=u'b', bottom=other_tot+guerilla_tot+aot_tot, width=.9)

#print(ax.get_children())
#import pdb; pdb.set_trace()
min_threshold = 400
all_tot = np.concatenate((other_tot, guerilla_tot, aot_tot, clear_tot))
all_num_events = np.concatenate((other_num_events, guerilla_num_events, aot_num_events, clear_num_events))
big_activities = all_tot > min_threshold
print(all_tot)
print(all_num_events)
all_num_events = all_num_events[big_activities]
all_tot = all_tot[big_activities]
print(all_tot)
print(all_num_events)
children = [child for child in ax.get_children() if isinstance(child, matplotlib.patches.Rectangle)]
children2 = [child for child in children if (child.get_bbox().y1 - child.get_bbox().y0 > min_threshold)]
for i, child in enumerate(children2):
    bbox = child.get_bbox()
    x = (bbox.x1 + bbox.x0)/2
    y = (bbox.y1 + bbox.y0)/2
    ax.text(x, y, "%d" % all_num_events[i], horizontalalignment='center', verticalalignment='center', color='w', transform=ax.transData)
    #sinstance(child, matplotlib.patch.Rectangle)
#ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
#ax.patch.set_facecolor('#FFFFFF')

plt.legend((p4[0], p3[0], p2[0], p1[0]), ('Lecture/Stargazing', 'Astronomy on Tap', 'Guerilla Astro', 'Special Events'))
plt.xlabel('Year')
ax.text(0.02, 0.72, "Includes Number of Events", horizontalalignment='left', verticalalignment='center', color='k', transform=ax.transAxes)
ax.text(0.02, 0.67, "For Each Category in White", horizontalalignment='left', verticalalignment='center', color='k', transform=ax.transAxes)
plt.ylabel('Number of Attendees')
plt.title('Caltech Astronomy Outreach Event Attendance By Year')
plt.savefig('caltech_histogram.pdf')
