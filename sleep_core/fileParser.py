'''
Created on Apr 30, 2014

'''
import csv
import os.path as path

from sleep_core.data import NightSession

_ext = '.csv'

class InvalidFileError(Exception):
    '''
    Raised if the file is the incorrect format.
    '''
    pass

def openFile(filePath):
    '''
    Verifies the file is a csv file, exists and hopefully the correct type of
    csv file. Creates and returns the reader object.
    '''
    if (path.splitext(filePath)[-1] != _ext or 
                path.exists(filePath) != True):
        raise InvalidFileError("Unable to open '%s' located at %s" 
                               %(path.basename(filePath),
                                 filePath))
    
    return Reader(filePath)
    
class Reader(object):
    '''
    Parses the csv file and separates the data into individual sessions as a
    list-list.
    '''
    
    def __init__(self, filePath):
        self.__file = filePath
        self.__rawData = []
        
        self.parse()
        
    def parse(self):
        '''
        Parses the csv file into individual night groups, puts this raw data
        into a list-list
        '''
        f = open(self.__file)
        data = csv.reader(f)
        
        night = []
        for row in data:
            # Skip over empty rows, possibly at the end of the file
            if len(row) == 0:
                continue
            # If the row contains the first item of 'Id' it's the start of a 
            # new entry.
            if row[0] == 'Id':
                self.__rawData.append(list(night))
                night = []
            night.append(row)
        # Append the very last night session
        self.__rawData.append(list(night))   
        
        # Check to make sure the first item in the list has data and not empty.
        if len(self.__rawData[0]) == 0:
            self.__rawData.pop(0)
           
        f.close()
        
    def getRawData(self):
        return self.__rawData
    
    def getSessions(self):
        '''
        Returns a list of NightSession objects.
        '''
        data = []
        for raw in self.__rawData:
            data.append(NightSession(raw))
        return data
            
        
        
        
