import os
from pythoncommons import property_reader_utils


def get_dictionary_by_profile(path, full_path=False):
    if not full_path:
        path = replace_relative_path(path, '/src/main/dao/filesystem',
                                     '/properties/profiles/')
    return property_reader_utils.make_dictionary(path)


def replace_relative_path(file_name, relative_target, relative_source):
    path = os.path.dirname(os.path.realpath(__file__))
    path = path.replace(relative_target, relative_source)
    path += file_name
    return path
