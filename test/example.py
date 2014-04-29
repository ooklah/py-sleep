'''

'''

import matplotlib.pyplot as plot
from dateutil import parser
import datetime

#def cleanup(d):
#    return d.split("    ")
#
#raw_time = "4:47    4:52    4:57    5:02    5:07    5:12    5:17    5:22    5:27    5:32    5:37    5:42    5:47    5:52    5:57    6:02    6:07    6:12    6:17    6:23    6:28    6:33    6:38    6:43    6:48    6:53    6:58    7:03    7:08    7:13    7:18    7:23    7:28    7:33    7:38    7:43    7:48    7:53    7:58    8:03    8:08    8:13    8:18    8:23    8:28    8:33    8:38    8:43    8:48    8:53    8:58    9:03    9:08    9:13    9:18    9:23    9:28    9:33    9:38    9:43    9:48    9:53    9:58    10:03    10:08    10:13    10:18    10:23    10:28    10:33    10:38    10:43    10:48    10:53    10:58    11:03    11:08    11:13    11:18    11:23    11:28    11:33    11:38    11:43    11:48    11:53    11:58    12:03    12:08"
#date = '2013-03-29'
#dates = [parser.parse('%s %s' %(date, s)) for s in cleanup(raw_time)]
#
#raw_points = "4.489956    4.489956    1.9717917    1.971812    0.029969871    0.0385833    0.15657628    0.15656957    1.0917426    1.0917497    0.03661922    0.03786147    0.0362646    0.039404936    0.039525665    0.18375313    1.038967    0.32961068    0.3296079    0.031585738    0.34063318    0.34061795    0.18407966    0.6694704    0.096055165    0.12286254    0.032779988    0.030466814    0.028564299    0.354064    0.35405594    0.6445054    0.64449257    0.39841607    0.36218387    0.45909855    0.12986116    1.437241    1.5936419    2.9734063    2.973646    0.08016849    0.41942856    0.7699858    0.6843533    1.07848    0.07854214    0.24817336    0.095596984    0.032684576    0.03730024    0.028661754    0.030909793    0.64964086    0.6516724    0.2674465    0.10209853    0.8632513    0.8633017    0.06997096    0.07005394    0.034117777    0.030009063    0.031782746    0.028532958    0.027819714    0.03267844    1.0454478    1.0455456    0.5366927    0.5367001    0.4088038    0.3236995    0.733793    0.903921    0.53983366    0.87370014    0.15887283    0.64080447    0.29504323    0.1699877    2.9123201    2.8426168    0.051310707    0.031364452    0.032076996    0.036016405    0.035631664    0.10947779"
#points = [float(s) for s in cleanup(raw_points)]
#
#plot.plot(dates, points)
#plot.show()

import csv
import os
import re

path = os.path.dirname(__file__)
f = open(os.path.join(path, 'sleep-export.csv'))

reader = csv.reader(f)

c = 0
sleeps = []

#for row in reader:
#    if row[0] == 'Id':
#        print 'New Item'
#        c += 1
#    if c == 2:
#        break;
#    print row

# Parsing the file, organizing it into nights
s = []
for row in reader:
    if row[0] == 'Id':
        if c != 0:
            sleeps.append(list(s))
            s = []
        c += 1
#    if c == 3:
#        break;
    s.append(row)
# appends very last row
sleeps.append(s)
    
from matplotlib.patches import Polygon
from matplotlib import dates as mt_date
from matplotlib import ticker
# Getting the time stamps out of the first line of the log
regex = r'\d{1,2}:\d{2}'

def adjustDates(dd):
    for n in range(len(dates)):
        dates[n] = dates[n] - dd

for i in range(185, len(sleeps)):
    raw_time = []
    for item in sleeps[i][0][14:len(sleeps[i][0])]:
        if re.match(regex, item, re.IGNORECASE):
            raw_time.append(item)
            
    points = []
    for item in sleeps[i][1][14:len(sleeps[i][1])]:
        try:
            points.append(float(item))
        except ValueError:
            pass
        
    raw_date = re.match(r'(\d{2}. \d{2}. \d{4})', sleeps[i][1][2]).group(1).replace(". ", "-")
    date = '-'.join(raw_date.split('-')[::-1])

    dates = [parser.parse('%s %s' %(date, s)) for s in raw_time]
            
    # Adjust time zone.
    if sleeps[i][1][1] == 'America/Los_Angeles':
        dd = datetime.timedelta(hours=3)
        adjustDates(dd)
    if sleeps[i][1][1] == 'America/Denver':
        dd = datetime.timedelta(hours=2)
        adjustDates(dd)
    if sleeps[i][1][1] == 'America/Chicago':
        dd = datetime.timedelta(hours=1)
        adjustDates(dd)

    
    print ("%s: %d" %(date, len(dates)))
    
    ax = plot.subplot(111, axisbg="#432b57")
    
    plot.plot(dates, points, linewidth=2, color="#132d78")
    
    #Make sure the ymin is 0 in case it wants to go below 0.
    plot.ylim(ymin=0)
    
    plot.title('Sleep Graph for %s' %date)
    plot.xlabel('Time of Day')
    plot.ylabel('Deep Sleep ---> Light Sleep')
    
    ax.xaxis.set_major_locator(mt_date.HourLocator())
    ax.xaxis.set_major_formatter(mt_date.DateFormatter('%H'))
    
    plot.fill_between(dates, points, facecolor="#335e3a")
#    plot.savefig(os.path.join(path, 'test/%s.png' %date))
    plot.show()
    plot.close()
    break;
f.close()

