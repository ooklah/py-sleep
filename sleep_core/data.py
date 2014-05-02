'''
Created on Apr 30, 2014

'''
#Map Values:
#    Id, (id, str)
#    Tz, (time zone)
#    From, (start time - 28. 03. 2014 0:58)
#    To,    (stop time - 28. 03. 2014 9:37)
#    Sched, (??? - 09. 04. 2014 1:38)
#    Hours, (total time slept, in float)
#    Rating, (rating, )
#    Comment, (tags and notes)
#    Framerate, (??? not sure what it's used for)
#    Snore,     (??? )
#    Noise,    (amount noise)
#    Cycles, (number of sleep cycles)
#    DeepSleep, (percent in float of deep sleep time)
#     LenAdjust, (??? )

import re
import datetime
from dateutil import parser


def findDate(rawStamp):
    '''
    Looks for a datestamp in the format of xx. xx. xxxx and returns it back
    a string as yyyy-mm-dd.
    '''
    rDateStamp = r'(\d{2}. \d{2}. \d{4})'
    rawDate = re.match(rDateStamp, rawStamp).group(1)
    return "-".join(rawDate.split(". ")[::-1])


def findTime(rawStamp):
    '''
    Looks for a timestamp in the format of x:xx or xx:xx and returns it back as
    a string with hh:mm.
    '''
    rTimeStamp = r'(\d{1,2}:\d{2})'
    rawTime = re.search(rTimeStamp, rawStamp).group()
    return rawTime

def cleanTimeStamp(rawStamp):
    '''
    Returns a cleaned up time stamp as a string: yyyy-mm-dd hh:mm
    '''
    return "%s %s" %(findDate(rawStamp), findTime(rawStamp))


class NightSession(object):
    '''
    Holds and allows easy access to the raw data supplied in list format.
    '''

    def __init__(self, raw):
        self.__data = raw
        self.map = dict(zip(self.__data[0][:14], self.__data[1][:14]))

    def getID(self):
        return int(self.map['Id'])

    def getTimeZone(self):
        return self.map['Tz']
    
    def __helperDate(self, value):
        return parser.parse("%s" %findDate(self.map[value]))
    
    def getStartTime(self):
        return parser.parse(cleanTimeStamp(self.map['From']))
        
    def getStartDate(self):
        return self.__helperDate('From')
    
    def getEndTime(self):
        return parser.parse(cleanTimeStamp(self.map['To']))
        
    def getEndDate(self):
        return self.__helperDate('To')
    
    def getSched(self):
        return parser.parse(cleanTimeStamp(self.map['Sched']))
    
    def getHours(self):
        return float(self.map['Hours'])
    
    def getRating(self):
        return float(self.map['Rating'])
    
    def getComment(self):
        return self.map['Comment']
    
    def getFrameRate(self):
        return int(self.map['Framerate'])
    
    def getSnore(self):
        return int(self.map['Snore'])
    
    def getNoise(self):
        return float(self.map['Noise'])
    
    def getCycles(self):
        return int(self.map['Cycles'])
    
    def getDeepSleep(self):
        return float(self.map['DeepSleep'])
    
    def getLenAdjust(self):
        return int(self.map['LenAdjust'])