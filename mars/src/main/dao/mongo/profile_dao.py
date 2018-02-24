from pythoncommons import mongo_utils, general_utils


def get_profile_collection(database):
    """Connects to the database and returns a pointer
    to the profiles collection.
    """
    connection = mongo_utils.mongo_get_connection(database)
    collection = mongo_utils.mongo_get_collection(connection, "mars_profiles")
    return collection


def create_profile_collection(database, profile):
    """Inserts the given profile into the profiles collection.
    Will automatically create the profiles collection if it does not exist.
    Returns the added profile.
    """
    collection = get_profile_collection(database)
    profile_id = mongo_utils.mongo_insert_one(collection, profile)
    return get_profile_by_id(database, profile_id)


def remove_profile_collection(database):
    """Completely blows away the profile collection.
    """
    collection = get_profile_collection(database)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_profile_by_name(database, name):
    """Returns the current profile by name.
    """
    collection = get_profile_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    profile_list = mongo_utils.unload_cursor(cursor)
    try:
        return profile_list[0]
    except IndexError:
        return None


def get_profile_by_id(database, profile_id):
    """Returns the current profile by name.
    """
    collection = get_profile_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('_id', profile_id))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    profile_list = mongo_utils.unload_cursor(cursor)
    try:
        return profile_list[0]
    except IndexError:
        return None


def get_default_profile(database):
    """Returns the current profile by name.
    """
    collection = get_profile_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('default', True))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    profile_list = mongo_utils.unload_cursor(cursor)
    try:
        return profile_list[0]
    except IndexError:
        return None

if __name__ == '__main__':
    print("Please use the profile dao module as method package.")
