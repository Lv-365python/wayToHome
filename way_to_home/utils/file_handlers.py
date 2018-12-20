"""This module implements helpers functions for work with files."""

import requests
import pickle


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
