'''
Created on Apr 30, 2014

'''
import unittest
import os
import datetime

from sleep_core.data import NightSession
from sleep_core import file as fp

path = os.path.dirname(__file__)
fyle = os.path.join(path, 'example-data.csv')

class TestNighSession(unittest.TestCase):
    
    def setUp(self):
        self.sessions = fp.openFile(fyle).getSessions()
        # one - type data that contains sound graph data
        self.one = self.sessions[0]
        # two - type data that does not have sound graph data
        
    def testGetID(self):
        self.assertEqual(self.one.getID(), 1395982691112)
        
    def testGetTimeZone(self):
        self.assertEqual(self.one.getTimeZone(), "America/New_York")
        
    def testGetStartDate(self):
        self.assertEqual(self.one.getStartDate(),
                         datetime.datetime(2014, 03, 28))

    def testGetStartTime(self):
        self.assertEqual(self.one.getStartTime(),
                         datetime.datetime(2014, 03, 28, 0, 58))
        
    def testGetEndDate(self):
        self.assertEqual(self.one.getEndDate(),
                         datetime.datetime(2014, 03, 28))
        
    def testGetEndTime(self):
        self.assertEqual(self.one.getEndTime(),
                         datetime.datetime(2014, 03, 28, 9, 37))
        
    def testGetSched(self):
        self.assertEqual(self.one.getSched(),
                         datetime.datetime(2014, 4, 9, 1, 38))
    def testGetHours(self):
        self.assertEqual(self.one.getHours(), 8.66)
        
    def testGetRating(self):
        self.assertEqual(self.one.getRating(), 0.9)
        
    def testGetComment(self):
        self.assertEqual(self.one.getComment(), "#comment here")
        
    def testGetFrameRate(self):
        self.assertEqual(self.one.getFrameRate(), 10000)
        
    def testGetSnore(self):
        self.assertEqual(self.one.getSnore(), -1)
        
    def testGetNoise(self):
        self.assertEqual(self.one.getNoise(), 0.043736402)
        
    def testGetCycles(self):
        self.assertEqual(self.one.getCycles(), 5)
        
    def testGetDeepSleep(self):
        self.assertEqual(self.one.getDeepSleep(), 0.40206185)
        
    def testGetLenAdjust(self):
        self.assertEqual(self.one.getLenAdjust(), -9)
        
    def testForValidSessionFromParser(self):
        self.assertIsInstance(self.one, NightSession)

    def testBasicGetSleepData(self):
        '''
        Test return for the sleep data. Make sure all the of the returned data
        is valid on the first and last cell.
        '''
        data = self.one.getSleepData()
        # Two rows lists of data
        self.assertEqual(len(data), 2)
        # Session should have 98 items in it
        self.assertEqual(len(data[0])+1, 98)
        print len(data[0])
        self.assertEqual(len(data[1])+1, 98)
        self.assertEqual(data[0][0], datetime.datetime(2014, 3, 28, 1, 3))
        self.assertEqual(data[0][96], datetime.datetime(2014, 3, 28, 9, 37))
        self.assertEqual(data[1][0], -0.01)
        self.assertEqual(data[1][96], 1.7762419)

class TestReader(unittest.TestCase):
    
    def testForValidData(self):
        reader = fp.openFile(fyle)
        raw = reader.getRawData()
        self.assertEqual(type(raw), type([]))
        # Two Sessions for the test data
        self.assertEqual(len(raw), 2)
        self.assert_( raw[0][0][0] == 'Id', raw[0][0][0])
        # Old, old data has only two rows of information
        # Newer rows have three rows. Using newer information
        self.assertEqual( len(raw[0]), 3, raw[0] )
        
    def testIsReaderObject(self):
        reader = fp.openFile(fyle)
        self.assertIsInstance(reader, fp.Reader)
    
    def testFileExists(self):
        fp.openFile(fyle)

    def testFileIsCSV(self):
        self.assertRaises(fp.InvalidFileError, fp.openFile, 'wrong-file.rsv')
        
    def testFileDoesNotExist(self):
        self.assertRaises(fp.InvalidFileError, fp.openFile, 'no-file.csv')


if __name__ == "__main__":
    unittest.main()