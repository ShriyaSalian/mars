import mars.src.main.model.generic_model as model_utils
import mars.src.main.processor.profile_processor as profile_processor


def make_search_dictionary(structure_directory, file_type):
    """Makes a dictionary for use in finding matching filetypes in a filesystem.
    """
    search_dictionary = {}
    search_dictionary['source_path'] = [structure_directory]
    search_dictionary['ends_with'] = ['.' + file_type]
    return search_dictionary


def get_fully_qualified_paths(database, target, profile=None):
    """Returns a target with any profile keywords filled in with the given profile.
    If no profile is specified, this method gets the default profile from the database.
    """
    profile = profile_processor.get_fully_qualified_profile(database, profile)
    path_getter = model_utils.replace_keywords_closure(profile)
    target = path_getter(target)
    return target


def adjust_property_value(value):
    if (isinstance(value, list) and len(value) == 1):
        return value[0]
    return value

if __name__ == '__main__':
    print('Please use generic processor module as method package.')
