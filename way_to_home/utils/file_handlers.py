"""This module implements helpers functions for work with files."""

import requests
import pickle


def _get_fields_position(row_header, required_fields):
    """
    Return dictionary where the keys are required fields and
    values are numbers of columns with the appropriate name.
    """
    fields_position = {}
    for field in required_fields:
        fields_position[field] = row_header.index(field)

    return fields_position


def load_file(url, save_to='./'):
    """Download file from `url` to directory with path `save_to`."""
    file_name = url.split('/')[-1]

    request = requests.get(url)
    if not request.status_code == 200:
        return False

    with open(f'{save_to}/{file_name}', 'wb') as file:
        file.write(request.content)

    return True


def pickle_data(data, path_to_file):
    """Write a pickled representation of data to file."""
    with open(path_to_file, 'wb') as file:
        pickle.dump(data, file)


def unpickle_data(path_to_file):
    """Read a pickled representation of data from file."""
    with open(path_to_file, 'rb') as file:
        data = pickle.load(file)

    return data
