from io import TextIOWrapper
import linecache
import math
import os
import datetime
from pathlib import Path


ISO_8601_RGX = "^\d{4}-(0\d|1[0-2])-([0-2]\d|3[0-2])(T(([01]\d|2[0-4]):([0-5]\d)(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])(:[0-5]\d([\.,]\d+)?)?|([01]\d|2[0-4])([\.,]\d+)?))?([+-]\d\d(:[0-5]\d)?|Z)?$"

class FileSearchService():
    dateStart: str
    dateEnd: str
    fileLength: int
    fileLocation: str

    def __init__(self, fileLocation: str, dateStart: str, dateEnd: str):
        self.dateStart = dateStart
        self.dateEnd = dateEnd
        self.fileLocation = f'/app/test-files/%s' %fileLocation
        print(self.fileLocation)
        
        f = open(self.fileLocation )
        line_count = 0
        for _ in f:
            line_count += 1
        self.fileLength = line_count
        f.close()

    def get_file_rows_by_date_range(self) -> list:
        rowsTouple = self.__file_date_search_recursive(0, self.fileLength -1)
        lines = []
        for i in range(rowsTouple[0], rowsTouple[1]):
            lines.append(self.__get_line(i))
        return list(map(self.__format_string, lines))
    
    def __get_line(self, line_number: int)-> str:
        line = linecache.getline(self.fileLocation, line_number)
        # We dont actually need lineCaches cache just the ability to read a single line
        linecache.clearcache()
        return line
    
    def __format_string(self, value:str) -> dict:
        values = value.split(' ')
        return {
            "eventTime": values[0].strip(),
            "email":values[1].strip(),
            "sessionId":values[2].strip()
        }

    def __file_date_search_recursive(self, start: int, end: int, startIdx: int = None) -> tuple[int, int] :
        if(start > end):
            return []
        middle = math.floor( (start + end) / 2)

        lineMiddle = self.__get_line(middle)
        linecache.clearcache()
        lineMiddlePrevious = self.__get_line(middle -1)
        linecache.clearcache()

        middleDateArgs = [
            int(lineMiddle[0:4]),
            int(lineMiddle[5:7]),
            int(lineMiddle[8:10]),
            int(lineMiddle[11:13]),
            int(lineMiddle[14:16]),
            int(lineMiddle[17:19])
        ]

        middlePreviousArgs = [
            int(lineMiddlePrevious[0:4]),
            int(lineMiddlePrevious[5:7]),
            int(lineMiddlePrevious[8:10]),
            int(lineMiddlePrevious[11:13]),
            int(lineMiddlePrevious[14:16]),
            int(lineMiddlePrevious[17:19])
        ]

        startDateArgs = [
            int(self.dateStart[0:4]),
            int(self.dateStart[5:7]),
            int(self.dateStart[8:10]),
            int(self.dateStart[11:13]),
            int(self.dateStart[14:16]),
            int(self.dateStart[17:19])
        ]

        endDateArgs = [
            int(self.dateEnd[0:4]),
            int(self.dateEnd[5:7]),
            int(self.dateEnd[8:10]),
            int(self.dateEnd[11:13]),
            int(self.dateEnd[14:16]),
            int(self.dateEnd[17:19])
        ]


        middleDate = datetime.datetime(*middleDateArgs)
        middlepreviousDate = datetime.datetime(*middlePreviousArgs)
        searchedDate = datetime.datetime(*startDateArgs) if startIdx is not None else datetime.datetime(*endDateArgs) 
        
        if middlepreviousDate < searchedDate <= middleDate:
            if startIdx is None:
                return self.__file_date_search_recursive(start, self.fileLength -1, middle)
            else:
                return (startIdx, middle)
        elif searchedDate < middleDate:
            if startIdx is None:
                return self.__file_date_search_recursive(start, middle -1)
            else:
                return self.__file_date_search_recursive(start, middle -1, startIdx)
        elif searchedDate > middleDate:
            if startIdx is None:
                return self.__file_date_search_recursive(middle +1, end)
            else: 
                return self.__file_date_search_recursive(middle +1, end, startIdx)

