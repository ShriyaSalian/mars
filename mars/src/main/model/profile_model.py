from pythoncommons import general_utils


def make_profile(profile, profile_dictionary, profile_name, full_path):
    """Adds information to a passed profile dictionary and returns it.
    """
    profile_dictionary = {key: profile_dictionary[key][0] for key in list(profile_dictionary.keys())}
    if full_path:
        profile_dictionary['name'] = profile_name
    else:
        profile_dictionary['name'] = profile
    profile_dictionary['type'] = 'path'
    profile_dictionary['default'] = False
    profile_dictionary['add_date'] = general_utils.get_timestamp()
    profile_dictionary['remove_date'] = None
    return profile_dictionary


def make_default_profile(profile, profile_dictionary, profile_name, full_path):
    """Adds information to a passed profile dictionary and returns it.
    """
    profile_dictionary = {key: profile_dictionary[key][0] for key in list(profile_dictionary.keys())}
    if full_path:
        profile_dictionary['name'] = profile_name
    else:
        profile_dictionary['name'] = profile
    profile_dictionary['type'] = 'path'
    profile_dictionary['default'] = True
    profile_dictionary['add_date'] = general_utils.get_timestamp()
    profile_dictionary['remove_date'] = None

    return profile_dictionary


def add_keys_to_existing_profile(profile_dictionary, default=True):
    """ Adds database keys to already existing profile.
    """
    profile_dictionary['name'] = 'default'
    profile_dictionary['type'] = 'path'
    profile_dictionary['add_date'] = general_utils.get_timestamp()
    profile_dictionary['remove_date'] = None
    profile_dictionary['default'] = default
    return profile_dictionary
