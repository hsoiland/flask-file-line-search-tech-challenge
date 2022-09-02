import unittest
from app.service import DateOrderError, FileSearchService, OutOfBoundsError
import pathlib
import os

class TestFileSearchService(unittest.TestCase):
    """
    Test the File Search Service
    """
    #TODO test the rest of the functions

    def test_search_first(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2000-01-01T17:25:49Z', '2000-01-01T17:25:49Z').get_file_rows_by_date_range()
        assert rows == [{'eventTime': '2000-01-01T17:25:49Z', 'email': 'dedric_strosin@adams.co.uk', 'sessionId': 'dfad33e7-f734-4f70-af29-c42f2b467142'}]


    def test_search_first_two(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2000-01-01T17:25:49Z', '2000-01-01T23:59:04Z').get_file_rows_by_date_range()
        assert rows == [{'eventTime': '2000-01-01T17:25:49Z', 'email': 'dedric_strosin@adams.co.uk', 'sessionId': 'dfad33e7-f734-4f70-af29-c42f2b467142'}, {'eventTime': '2000-01-01T23:59:04Z', 'email': 'abner@bartolettihills.com', 'sessionId': 'b3daf720-6112-4a49-9895-62dda13a2932'}]

    
    def test_search_first_three(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2000-01-01T17:25:49Z', '2000-01-02T20:59:05Z').get_file_rows_by_date_range()
        assert rows == [{'eventTime': '2000-01-01T17:25:49Z', 'email': 'dedric_strosin@adams.co.uk', 'sessionId': 'dfad33e7-f734-4f70-af29-c42f2b467142'}, {'eventTime': '2000-01-01T23:59:04Z', 'email': 'abner@bartolettihills.com', 'sessionId': 'b3daf720-6112-4a49-9895-62dda13a2932'}, {'eventTime': '2000-01-02T20:59:05Z', 'email': 'janis_nienow@johnson.name', 'sessionId': '1f90471c-adc3-4daa-9a6d-ff9d184b7a61'}]

    
    def test_search_last(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2001-07-14T17:14:40Z', '2001-07-14T17:14:40Z').get_file_rows_by_date_range()
        assert rows == [{'eventTime': '2001-07-14T17:14:40Z', 'email': 'howard@lebsackprosacco.co.uk', 'sessionId': 'fc5621fa-212b-4750-8606-7dbc21c94f26'}]

    def test_search_range(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2001-06-25T00:56:45Z', '2001-06-28T18:13:54Z').get_file_rows_by_date_range()
        assert rows == [{'eventTime': '2001-06-25T00:56:47Z', 'email': 'zachariah_koepp@wuckertstreich.biz', 'sessionId': 'fbf3c081-145c-49ec-9dfa-befde155ef26'}, {'eventTime': '2001-06-25T17:25:18Z', 'email': 'theresia.torphy@dooley.us', 'sessionId': '0fee583a-af84-4c97-8396-3b42190734ca'}, {'eventTime': '2001-06-26T17:25:28Z', 'email': 'santos@shanahan.uk', 'sessionId': '9d49e5e6-034f-4a7f-b1b9-09d1d99a48ff'}, {'eventTime': '2001-06-27T10:42:00Z', 'email': 'spencer@anderson.biz', 'sessionId': '523463f4-97d5-46ce-b9ca-2753613fc9da'}, {'eventTime': '2001-06-28T14:04:15Z', 'email': 'joan@hackettbogisich.us', 'sessionId': '1a4bf32c-8e94-4ec4-a6ad-019e091b5c31'}, {'eventTime': '2001-06-28T18:13:53Z', 'email': 'lavinia@schoen.uk', 'sessionId': '73065987-c1ef-4a5b-be21-63aa9d4141c9'}]

    def test_search_start_out_of_end_range(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        with self.assertRaises(DateOrderError):
            FileSearchService(path, '2001-07-14T17:15:40Z', '2001-07-14T17:15:40Z').get_file_rows_by_date_range()
        
    def test_search_end_out_of_start_range(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        with self.assertRaises(DateOrderError):
            FileSearchService(path, '2000-01-01T17:25:00Z', '2000-01-01T17:25:00Z').get_file_rows_by_date_range()
    
    def test_search_start_end_swapped(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        with self.assertRaises(DateOrderError):
            FileSearchService(path, '2001-06-28T18:13:54Z', '2001-06-25T00:56:45Z').get_file_rows_by_date_range()
    
    def test_search_dates_before_and_after_dataset(self):
        path = pathlib.Path(__file__).parent.parent.resolve()
        path = os.path.join(path, 'test-files/test1.txt')
        rows = FileSearchService(path, '2000-01-01T17:25:00Z', '2001-07-14T17:15:40Z').get_file_rows_by_date_range()
        assert rows.__len__() == 1000

if __name__ == '__main__':
    unittest.main()        