import mars.src.main.dao.filesystem.filesystem_dao as file_dao
import mars.src.main.model.profile_model as profile_model
import mars.src.main.dao.mongo.profile_dao as profile_dao
from pythoncommons import general_utils


def make_profile_from_filesystem(profile=None, default=False, full_path=True, profile_name=None):
    """Takes the name of a profile and uses that to create a profile dictionary.
    If default is set to true, this will be added as a default profile.
    """
    profile_dictionary = file_dao.get_dictionary_by_profile(profile, full_path=full_path)
    if default:
        profile = profile_model.make_default_profile(profile, profile_dictionary, profile_name, full_path)
    else:
        profile = profile_model.make_profile(profile, profile_dictionary, profile_name, full_path)
    return profile


def remove_profile_collection(database):
    """Completely removes a profile collection from storage in the specified database.
    """
    return profile_dao.remove_profile_collection(database)


def get_fully_qualified_profile(database, profile=None):
    if profile:
        profile = get_profile_by_name(database, profile)
    else:
        profile = get_default_profile(database)
    try:
        utils.get_fully_qualified_dictionary_values(profile)
    except:
        pass
    return profile


def create_profile_collection(database, profile):
    """Adds the given profile to the database. Returns the newly inserted profile record.
    """
    profile_dao.remove_profile_collection(database)
    profile = profile_dao.create_profile_collection(database, profile)
    return profile


def get_profile_by_name(database, profile_name):
    """Gets a profile by the specified name from the database.
    Returns the profile object.
    """
    profile = profile_dao.get_profile_by_name(database, profile_name)
    return profile


def get_default_profile(database):
    """Returns the default profile from the database.
    """
    profile = profile_dao.get_default_profile(database)
    return profile


def add_profile_from_filesystem(database, profile=None, full_path=True, profile_name=None, profile_dictionary=None):
    """Gets the specified profile from the filesystem for the given name.
    """
    if profile_dictionary:
        profile = profile_dictionary
        profile = profile_model.add_keys_to_existing_profile(profile)
    else:
        profile = make_profile_from_filesystem(profile=profile, default=True, full_path=full_path, profile_name=profile_name)
    profile = create_profile_collection(database, profile)
    profile = get_default_profile(database)
    return profile
