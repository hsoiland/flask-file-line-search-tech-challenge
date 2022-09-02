import linecache
import math
import datetime
import logging
import re

# Regex string for the iso 8601 date
ISO_8601_RGX = "^\d{4}-(0\d|1[0-2])-([0-2]\d|3[0-2])(T(([01]\d|2[0-4]):([0-5]\d)(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])([\.,]\d+)?))?([+-]\d\d(:[0-5]\d)?|Z)?$"

#Custom errors for class handling and easier testing
class Error(Exception):
    pass

class IncorrectDateType(Error):
    pass

class OutOfBoundsError(Error):
    pass

class FileError(Error):
    pass

class DateOrderError(Error):
    pass    

class FileSearchService():
    datestart: str
    dateend: str
    filelength: int
    filelocation: str

    """
    Validate the date ad get the line count
    """
    def __init__(self, filelocation: str, datestart: str, dateend: str):
        self.datestart = datestart
        self.dateend = dateend
        self.filelocation = filelocation

        # Check if the date is valid
        if not self.__valid_date(datestart) and not self.__valid_date(dateend):
            logging.error('FileSearchService - __init__: Dates not ISO_8601')
            raise IncorrectDateType('Dates not ISO_8601')

        # Check boundaries
        if self.__get_date_from_string(dateend) < self.__get_date_from_string(datestart):
            logging.error('FileSearchService - __init__: End date is earlier than start date')
            raise DateOrderError("End date is less than start date")

        if self.__get_date_from_string(dateend) < self.__get_date_from_string(self.__get_line(1)):
            logging.error('FileSearchService - __init__: End date is earlier than first item')
            raise DateOrderError("End date is earlier than first item")

        try: 
            # TODO
            # I Had an idea where we could look for the midpoints for the recursion based search on the 
            # approximate middle line using the middle of the number of bytes or a approx bytes per line and the closest new line 
            # a bit of over kill but would remove needing to iterate the whole file here
            f = open(self.filelocation)
            linecount = 0
            for _ in f:
                linecount += 1
            self.filelength = linecount
            f.close()
        except:
            logging.error("FileSearchService - __init__: Error opening file")
            raise FileError("Error opening file")

        # Check boundaries
        if self.__get_date_from_string(datestart) > self.__get_date_from_string(self.__get_line(self.filelength)):
            logging.error('FileSearchService - __init__: Start date is after the last item')
            raise DateOrderError("Start date is after the last item")
    
    """
    Date validation
    """
    def __valid_date(self, date: str)-> bool:
        return re.search(ISO_8601_RGX, date) is not None

    """
    Convert the input iso 8601 string to a date
    """
    def __get_date_from_string(self, datestring: str)-> datetime:
        dateargs = [
            int(datestring[0:4]),
            int(datestring[5:7]),
            int(datestring[8:10]),
            int(datestring[11:13]),
            int(datestring[14:16]),
            int(datestring[17:19])
        ]
        return datetime.datetime(*dateargs)

    """
    Main service function. Binary search for the start date and get the rows until the end date
    """
    def get_file_rows_by_date_range(self) -> list:
        startrow: int
        # If the start date is before the start of the data just take the first element instead of recursing
        if self.__get_date_from_string(self.datestart) < self.__get_date_from_string(self.__get_line(1)):
            startrow = 1
        else:
            # Get the start index in the file
            startrow = self.__file_date_search_recursive(1, self.filelength)

        # Go through the range and add the lines
        lines = []
        for i in range(startrow, self.filelength + 1):
            line = self.__get_line(i)
            if self.__get_date_from_string(line) > self.__get_date_from_string(self.dateend):
                break
            lines.append(self.__get_line(i))
        # Format the string and return
        return list(map(self.__format_string, lines))
    
    """
    Given a line number get the line using linecache(fast) but dont cache as we want to conserve memory
    """
    def __get_line(self, linenumber: int)-> str:
        line = linecache.getline(self.filelocation, linenumber)
        # We dont actually need lineCaches cache just the ability to read a single line
        linecache.clearcache()
        return line

    """
    Format the string to a dictionary
    """
    def __format_string(self, value:str) -> dict:
        values = value.split(' ')
        return {
            "eventTime": values[0].strip(),
            "email":values[1].strip(),
            "sessionId":values[2].strip()
        }

    """
    Binary search to find the start date
    """
    def __file_date_search_recursive(self, start: int, end: int) -> int:
        # Base exit
        if(start > end):
            logging.error("FileSearchService - __file_date_search_recursive: search is out of bounds")
            raise OutOfBoundsError("Out of bounds")

        # mid point 
        middle = math.floor( (start + end) / 2)

        linemiddle = self.__get_line(middle)
        # item before the middle line but not less than 1
        linemiddleprevious = self.__get_line(middle -1) if middle > 1 else self.__get_line(middle)

        # the dates in daetime format
        middledate = self.__get_date_from_string(linemiddle)
        middlepreviousdate = self.__get_date_from_string(linemiddleprevious)
        searcheddate = self.__get_date_from_string(self.datestart)

        # if the date matches or is in between our middle and the item before return middle
        if middlepreviousdate <= searcheddate <= middledate:
            return middle
        # elif the date is less go left
        elif searcheddate < middledate:
            return self.__file_date_search_recursive(start, middle -1)
        # else the date is larger go right
        else:
            return self.__file_date_search_recursive(middle + 1, end)


