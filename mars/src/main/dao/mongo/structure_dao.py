from pythoncommons import mongo_utils, general_utils


def get_structure_collection(database):
    """Connects to the database and returns a pointer
    to the structures collection.
    """
    connection = mongo_utils.mongo_get_connection(database)
    collection = mongo_utils.mongo_get_collection(connection, "mars_structures")
    return collection


def add_structure(database, structure):
    """Adds a single structure to the structure collection for the given database.
    """
    collection = get_structure_collection(database)
    structure_id = mongo_utils.mongo_insert_one(collection, structure)
    return get_structure_by_id(database, structure_id)


def create_structure_collection(database, structures):
    """Inserts all the given structures into the structures collection.
    Will automatically create the structures collection if it does not exist.
    Returns the structures in the collection.
    """
    collection = get_structure_collection(database)
    record_ids = mongo_utils.mongo_insert_many(collection, structures)
    return record_ids


def remove_structure_collection(database):
    """Completely blows away the structure collection.
    """
    collection = get_structure_collection(database)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_all_structures(database, args=None):
    """Returns all the structures in storage.
    """
    collection = get_structure_collection(database)
    if args:
        arguments = [mongo_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
        argument = general_utils.merge_list_of_dicts(arguments)
        cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    else:
        cursor = mongo_utils.mongo_find_records(collection)
    return mongo_utils.unload_cursor(cursor)


def get_current_structures(database, args=None):
    """Returns all the structures that haven't been removed.
    """
    collection = get_structure_collection(database)
    arguments = []
    if args:
        arguments = [mongo_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
    arguments.append(mongo_utils.make_single_field_argument("remove_date", None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    return mongo_utils.unload_cursor(cursor)


def get_structure_by_name(database, name):
    """Returns the current structure by name.
    """
    collection = get_structure_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    structure_list = mongo_utils.unload_cursor(cursor)
    try:
        return structure_list[0]
    except IndexError:
        return None


def get_structure_by_id(database, structure_id):
    """Returns the current profile by name.
    """
    structure_id = mongo_utils.ensure_objectid(structure_id)
    collection = get_structure_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('_id', structure_id))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    structure_list = mongo_utils.unload_cursor(cursor)
    try:
        return structure_list[0]
    except IndexError:
        return None


def update_structure(database, structure, changes):
    """Updates the given structure by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_structure_collection(database)
    structure_id = mongo_utils.ensure_objectid(structure['_id'])
    argument = mongo_utils.make_single_field_argument('_id', structure_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'structure'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(mongo_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(mongo_utils.make_update_argument(change, structure[change]))
    update = mongo_utils.merge_update_args(updates)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_structure_by_id(database, structure_id)
    return None


if __name__ == '__main__':
    print("Please use the structure dao module as method package.")
