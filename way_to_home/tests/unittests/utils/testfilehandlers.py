"""
File handlers Test
========================
This module provides complete testing for all file handlers.
"""
import csv
import pickle
from unittest.mock import patch, mock_open
from zipfile import BadZipFile

from django.test import TestCase

from utils.file_handlers import (unzip_file,
                                 load_file,
                                 pickle_data,
                                 unpickle_data,
                                 parse_csv_file,
                                 _get_fields_position)


class MockZipFile:
    def __init__(self, *args, **kwargs):
        pass

    def extractall(self, *args, **kwargs):
        return True


class MockRequests:
    def success(self, *args, **kwargs):
        return MockRequestSussess()

    def error(self, *args, **kwargs):
        return MockRequestError()


class MockRequestError:
    status_code = 400


class MockRequestSussess:
    status_code = 200
    content = ''


class MockCSV:
    def __init__(self):
        self.line_num = 0
        self.size = 2

    def __iter__(self):
        return self

    def __next__(self):
        if self.line_num >= self.size:
            raise StopIteration
        else:
            self.line_num += 1
            return {1: 'value1',
                    2: 'value2',
                    3: 'value3'}


class FileHandlersTestCase(TestCase):
    """Test Case that provides tests for file handlers"""
    def test_get_fields_position(self):
        """Method that tests the _get_fields_position function"""
        test_header = ['field2', 'field3', 'field1']
        test_required_fields = ['field1', 'field2', 'field3']

        result = _get_fields_position(test_header, test_required_fields)
        expected_result = {'field1': 2,
                           'field2': 0,
                           'field3': 1}
        self.assertEqual(result, expected_result)

    @patch('utils.file_handlers.ZipFile.__init__', MockZipFile.__init__)
    @patch('utils.file_handlers.ZipFile.extractall', MockZipFile.extractall)
    def test_unzip_file_valid(self):
        """Method that tests the unzip_file function with valid data"""
        result = unzip_file('file_path')
        self.assertTrue(result)

    @patch('utils.file_handlers.ZipFile.__init__', MockZipFile.__init__)
    def test_unzip_file_extract_exception(self):
        """Method that tests the extract exceptions in unzip_file function"""
        exceptions = (ValueError, BadZipFile, PermissionError)

        with patch('utils.file_handlers.ZipFile.extractall') as extract:
            for exc in exceptions:
                extract.side_effect = exc()
                result = unzip_file('file_path')
                self.assertFalse(result)

    def test_unzip_file_zipfile_exception(self):
        """Method that tests the ZipFile exceptions in unzip_file function"""
        exceptions = (FileNotFoundError, PermissionError)

        with patch('utils.file_handlers.ZipFile.__init__') as zip_file:
            for exc in exceptions:
                zip_file.side_effect = exc()
                result = unzip_file('file_path')
                self.assertFalse(result)

    @patch('utils.file_handlers.requests.get', MockRequests.success)
    @patch('builtins.open', mock_open(read_data="data"))
    @patch('typing.BinaryIO.write', return_value=True)
    def test_load_file_valid(self, write):
        """Method that tests the load_file function with valid data"""
        loaded = load_file('url')
        self.assertIsNotNone(loaded)

    @patch('utils.file_handlers.requests.get', MockRequests.success)
    def test_load_file_permission_error(self):
        """Method that tests the PermissionError exception load_file function"""
        with patch('builtins.open') as open_file:
            open_file.side_effect = PermissionError()
            loaded = load_file('url')
            self.assertIsNone(loaded)

    @patch('utils.file_handlers.requests.get', MockRequests.error)
    def test_load_file_error_status_code(self):
        """Method that tests the load_file function with error status code"""
        loaded = load_file('url')
        self.assertIsNone(loaded)

    @patch('builtins.open', mock_open(read_data="data"))
    @patch('utils.file_handlers.csv.reader')
    @patch('utils.file_handlers._get_fields_position')
    def test_parse_csv_file_valid(self, fields_position, csv_reader):
        """Method that tests the parse_csv_file function with valid data"""
        csv_reader.return_value = MockCSV()
        fields_position.return_value = {'key1': 1,
                                        'key2': 2,
                                        'key3': 3}
        result = parse_csv_file('path', [])
        self.assertIsNotNone(result)

    @patch('builtins.open', mock_open(read_data="data"))
    def test_parse_csv_csv_exception(self):
        """Method that tests the csv.Error in parse_csv_file function"""
        with patch('utils.file_handlers.csv.reader') as csv_file:
            csv_file.side_effect = csv.Error()
            result = parse_csv_file('path', [])
            self.assertIsNone(result)

    def test_parse_csv_file_open_exception(self):
        """Method that tests the open() exceptions in parse_csv_file function"""
        exceptions = (FileNotFoundError, PermissionError)

        with patch('builtins.open') as open_file:
            for exc in exceptions:
                open_file.side_effect = exc()
                result = parse_csv_file('path', [])
                self.assertIsNone(result)

    @patch('builtins.open', mock_open(read_data="data"))
    @patch('utils.file_handlers.pickle.dump', return_data=True)
    def test_pickle_data_valid(self, pickle):
        """Method that tests the pickle_data function with valid data"""
        pickled = pickle_data({}, 'path')
        self.assertTrue(pickled)

    @patch('builtins.open', mock_open(read_data="data"))
    def test_pickle_data_exceptions(self):
        """Method that tests the pickle exceptions in pickle_data function"""
        exceptions = (pickle.PicklingError, PermissionError)

        with patch('utils.file_handlers.pickle.dump') as pickled_data:
            for exc in exceptions:
                pickled_data.side_effect = exc()
                result = pickle_data({}, 'path')
                self.assertFalse(result)

    @patch('builtins.open', mock_open(read_data="data"))
    @patch('utils.file_handlers.pickle.load', return_data=True)
    def test_unpickle_data_valid(self, pickle):
        """Method that tests the unpickle_data function with valid data"""
        pickled = unpickle_data('path')
        self.assertIsNotNone(pickled)

    @patch('builtins.open', mock_open(read_data="data"))
    def test_unpickle_data_pickle_exception(self):
        """Method that tests the pickle.UnpicklingError exception in unpickle_data function"""
        with patch('utils.file_handlers.pickle.load') as unpickled_data:
            unpickled_data.side_effect = pickle.UnpicklingError()
            result = unpickle_data('path')
            self.assertIsNone(result)

    def test_unpickle_data_open_exceptions(self):
        """Method that tests the open() exceptions in unpickle_data function"""
        exceptions = (FileNotFoundError, PermissionError)

        with patch('builtins.open') as open_file:
            for exc in exceptions:
                open_file.side_effect = exc()
                result = unpickle_data('path')
                self.assertIsNone(result)
