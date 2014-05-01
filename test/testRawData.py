'''
Created on Apr 30, 2014

'''
import unittest
import os
import datetime

from sleep_core.data import NightSession
from sleep_core import fileParser as fp

path = os.path.dirname(__file__)
fyle = os.path.join(path, 'example-data.csv')

class TestNighSession(unittest.TestCase):
    
    def setUp(self):
        self.sessions = fp.openFile(fyle).getSessions()
        
    def testGetID(self):
        self.assertEqual(self.sessions[0].getID(), 1395982691112)
        
    def testGetTimeZone(self):
        self.assertEqual(self.sessions[0].getTimeZone(), "America/New_York")
        
    def testGetStartDate(self):
        self.assertEqual(self.sessions[0].getStartDate(),
                         datetime.datetime(2014, 03, 28))

    def testGetStartTime(self):
        self.assertEqual(self.sessions[0].getStartTime(),
                         datetime.datetime(2014, 03, 28, 0, 58))
        
    def testGetEndDate(self):
        self.assertEqual(self.sessions[0].getEndDate(),
                         datetime.datetime(2014, 03, 28))
        
    def testGetEndTime(self):
        self.assertEqual(self.sessions[0].getEndTime(),
                         datetime.datetime(2014, 03, 28, 9, 37))
        
    def testForValidSessionFromParser(self):
        self.assertIsInstance(self.sessions[0], NightSession)


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