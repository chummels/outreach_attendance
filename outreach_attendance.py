#!/usr/bin/env python
'''
This script is for generating two figures associated with the attendance
at various outreach activities throughout the year.  One is a histogram
of outreach events per year and their total attendance, the other is just
a scatter plot showing attendance at each event as a function of date.

The input for this script is a text file listing each event as a 
separate line employing the following format:

# month day year attendees event_code
# where event_code is: 
0 = lecture/stargazing
2 = astro on tap
3 = special event (eclipse, science fair)
4 = guerilla astronomy
5 = foreign language

Example:

03 24 2011   20 3
07 19 2013  100 0
10 17 2016  130 2

Run script as:

$ python outreach_attenance.py caltech.txt
'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.ticker
import datetime
import numpy as np
import sys

# Input data from text file
if len(sys.argv) != 2:
    print("Usage: python %s <input.txt>" % sys.argv[0])
    sys.exit()
input_file = sys.argv[1]
output_prefix = input_file.split('.')[0]
data = np.genfromtxt(input_file, dtype="int32")
month = data[:,0]
day = data[:,1]
year = data[:,2]
number = data[:,3]
code = data[:,4]

start_year = data[:,2].min()
end_year = data[:,2].max()
start = datetime.date(start_year, 1, 1)
end = datetime.date(end_year, 12, 31)

# Force the start and end dates for the plotting range
# Uncomment to use; otherwise defined automatically from input
#start = datetime.date(2011, 1, 1)
#end = datetime.date(2019, 4, 1)
startnum = matplotlib.dates.date2num(start)
endnum = matplotlib.dates.date2num(end)
cameron_start = datetime.date(2015, 10, 1)
cameron_text = datetime.date(2015, 11, 1)
pandemic_start = datetime.date(2020, 3, 15)
pandemic_text = datetime.date(2020, 4, 15)
pandemic_end = datetime.date(2022, 6, 15)
pandemic_end_text = datetime.date(2022, 7, 15)
cameron_start_num = matplotlib.dates.date2num(cameron_start)
cameron_text_num = matplotlib.dates.date2num(cameron_text)
pandemic_start_num = matplotlib.dates.date2num(pandemic_start)
pandemic_text_num = matplotlib.dates.date2num(pandemic_text)
pandemic_end_num = matplotlib.dates.date2num(pandemic_end)
pandemic_end_text_num = matplotlib.dates.date2num(pandemic_end_text)

# Create empty arrays for plotting against each other
dates = []
lecture_dates = []
lecture_num = []
aot_dates = []
aot_num = []
other_dates = []
other_num = []
guerilla_dates = []
guerilla_num = []
foreign_dates = []
foreign_num = []

# Populate the arrays with appropriate dates and corresponding turnout
for i in range(len(month)):
	temp_date = datetime.date(year[i],month[i],day[i])
	new_date =  matplotlib.dates.date2num(temp_date)
	if (code[i] == 0):
		lecture_dates.append(new_date)
		lecture_num.append(number[i])
		dates.append(new_date)
	elif (code[i] == 2):
		aot_dates.append(new_date)
		aot_num.append(number[i])
		dates.append(new_date)
	elif (code[i] == 3):
		other_dates.append(new_date)
		other_num.append(number[i])
		dates.append(new_date)
	elif (code[i] == 4):
		guerilla_dates.append(new_date)
		guerilla_num.append(number[i])
		dates.append(new_date)
	elif (code[i] == 5):
		foreign_dates.append(new_date)
		foreign_num.append(number[i])
		dates.append(new_date)

# Plot the stuff!
if len(lecture_dates) > 0:
    plt.plot_date(lecture_dates, lecture_num, 'bo', label='Lecture/Stargazing', alpha=0.6)
if len(aot_dates) > 0:
    plt.plot_date(aot_dates, aot_num, 'go', label='Astronomy on Tap', alpha=0.6)
if len(guerilla_dates) > 0:
    plt.plot_date(guerilla_dates, guerilla_num, 'yo', label='Guerilla Astro', alpha=0.6)
if len(other_dates) > 0:
    plt.plot_date(other_dates, other_num, 'ro', label='Special Event', alpha=0.6)
if len(foreign_dates) > 0:
    plt.plot_date(foreign_dates, foreign_num, 'mo', label='Foreign Language', alpha=0.6)
plt.legend(loc=2, numpoints=1)
plt.xlabel('Date')
plt.ylabel('Number of Attendees')
plt.title('%s Astronomy Outreach Event Attendance' % output_prefix.capitalize())
locator = matplotlib.dates.YearLocator()
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()
ax = plt.gca()
ax.set_yscale('log')
ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.axis([startnum, endnum, 10, 10000])
plt.plot([cameron_start_num, cameron_start_num], [10,10000], color='k')
plt.text(cameron_text_num, 300, 'CBH Begins at Caltech', rotation='vertical', color='k', weight='book')
plt.plot([pandemic_start_num, pandemic_start_num], [10,10000], color='k')
plt.text(pandemic_text_num, 800, 'Pandemic Begins', rotation='vertical', color='k', weight='book')
#plt.plot([pandemic_end_num, pandemic_end_num], [10,10000], color='k')
#plt.text(pandemic_end_text_num, 300, 'Restart In-Person Events', rotation='vertical', color='k', weight='book')
plt.savefig('%s_timeline.png' % output_prefix)

# Histogram plot
year_range = list(range(start.year, end.year+1))
lecture_tot = np.empty(len(year_range))
aot_tot = np.empty(len(year_range))
guerilla_tot = np.empty(len(year_range))
other_tot = np.empty(len(year_range))
foreign_tot = np.empty(len(year_range))
lecture_num_events = np.empty(len(year_range))
aot_num_events = np.empty(len(year_range))
guerilla_num_events = np.empty(len(year_range))
other_num_events = np.empty(len(year_range))
foreign_num_events = np.empty(len(year_range))

# Add up each category of events
for i, year in enumerate(year_range):
    num_attendees = 0
    num_events = 0
    for j in range(len(lecture_dates)):
        if matplotlib.dates.num2date(lecture_dates[j]).year == year:
            num_attendees += lecture_num[j]
            num_events += 1
    lecture_tot[i] = num_attendees    
    lecture_num_events[i] = num_events
    num_attendees = 0
    num_events = 0
    for j in range(len(aot_dates)):
        if matplotlib.dates.num2date(aot_dates[j]).year == year:
            num_attendees += aot_num[j]
            num_events += 1
    aot_tot[i] = num_attendees    
    aot_num_events[i] = num_events
    num_attendees = 0
    num_events = 0
    for j in range(len(guerilla_dates)):
        if matplotlib.dates.num2date(guerilla_dates[j]).year == year:
            num_attendees += guerilla_num[j]
            num_events += 1
    guerilla_tot[i] = num_attendees    
    guerilla_num_events[i] = num_events
    num_attendees = 0
    num_events = 0
    for j in range(len(other_dates)):
        if matplotlib.dates.num2date(other_dates[j]).year == year:
            num_attendees += other_num[j]
            num_events += 1
    other_tot[i] = num_attendees    
    other_num_events[i] = num_events
    num_attendees = 0
    num_events = 0
    for j in range(len(foreign_dates)):
        if matplotlib.dates.num2date(foreign_dates[j]).year == year:
            num_attendees += foreign_num[j]
            num_events += 1
    foreign_tot[i] = num_attendees
    foreign_num_events[i] = num_events

# Plot the histogram stuff!
fig, ax = plt.subplots(1,1)
p0 = plt.bar(year_range, foreign_tot, color=u'm', width=.9)
p1 = plt.bar(year_range, other_tot, color=u'r', bottom=foreign_tot, width=.9)
p2 = plt.bar(year_range, guerilla_tot, color=u'y', bottom=foreign_tot+other_tot, width=.9)
p3 = plt.bar(year_range, aot_tot, color=u'g', bottom=foreign_tot+other_tot+guerilla_tot, width=.9)
p4 = plt.bar(year_range, lecture_tot, color=u'b', bottom=foreign_tot+other_tot+guerilla_tot+aot_tot, width=.9)
total = 0
for i,year in enumerate(year_range):
    print("%d: %d events; %d attendees" % (year_range[i], \
        foreign_num_events[i]+other_num_events[i]+guerilla_num_events[i]+aot_num_events[i]+lecture_num_events[i], \
        foreign_tot[i]+other_tot[i]+guerilla_tot[i]+aot_tot[i]+lecture_tot[i]))
    total += foreign_tot[i]+other_tot[i]+guerilla_tot[i]+aot_tot[i]+lecture_tot[i]
print("Total Events: %d" % total)
print("Total Attendance: %d" % total)

min_threshold = 250
all_tot = np.concatenate((foreign_tot, other_tot, guerilla_tot, aot_tot, lecture_tot))
all_num_events = np.concatenate((foreign_num_events, other_num_events, guerilla_num_events, aot_num_events, lecture_num_events))
big_activities = all_tot > min_threshold
all_num_events = all_num_events[big_activities]
all_tot = all_tot[big_activities]
children = [child for child in ax.get_children() if isinstance(child, matplotlib.patches.Rectangle)]
children2 = [child for child in children if (child.get_bbox().y1 - child.get_bbox().y0 > min_threshold)]
for i, child in enumerate(children2):
    bbox = child.get_bbox()
    x = (bbox.x1 + bbox.x0)/2
    y = (bbox.y1 + bbox.y0)/2
    ax.text(x, y, "%d" % all_num_events[i], horizontalalignment='center', verticalalignment='center', color='w', transform=ax.transData)

plt.legend((p4[0], p3[0], p2[0], p1[0], p0[0]), ('Lecture/Stargazing', 'Astronomy on Tap', 'Guerilla Astro', 'Special Events', 'Foreign Language'), loc=2)
plt.xlabel('Year')
ax.text(0.02, 0.65, "Includes Number of Events", horizontalalignment='left', verticalalignment='center', color='k', transform=ax.transAxes)
ax.text(0.02, 0.60, "For Each Category in White", horizontalalignment='left', verticalalignment='center', color='k', transform=ax.transAxes)
plt.ylabel('Number of Attendees')
plt.title('%s Astronomy Outreach Event Attendance By Year' % output_prefix.capitalize())
plt.savefig('%s_histogram.png' % output_prefix)
