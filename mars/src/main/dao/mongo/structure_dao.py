from python_commons import db_utils, utils


def get_structure_collection(database):
    """Connects to the database and returns a pointer
    to the structures collection.
    """
    connection = db_utils.mongo_get_connection(database)
    collection = db_utils.mongo_get_collection(connection, "mars_structures")
    return collection


def add_structure(database, structure):
    """Adds a single structure to the structure collection for the given database.
    """
    collection = get_structure_collection(database)
    structure_id = db_utils.mongo_insert_one(collection, structure)
    return get_structure_by_id(database, structure_id)


def create_structure_collection(database, structures):
    """Inserts all the given structures into the structures collection.
    Will automatically create the structures collection if it does not exist.
    Returns the structures in the collection.
    """
    collection = get_structure_collection(database)
    record_ids = db_utils.mongo_insert_many(collection, structures)
    return record_ids


def remove_structure_collection(database):
    """Completely blows away the structure collection.
    """
    collection = get_structure_collection(database)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_all_structures(database, args=None):
    """Returns all the structures in storage.
    """
    collection = get_structure_collection(database)
    if args:
        arguments = [db_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
        argument = utils.merge_list_of_dicts(arguments)
        cursor = db_utils.mongo_find_records(collection, argument=argument)
    else:
        cursor = db_utils.mongo_find_records(collection)
    return db_utils.unload_cursor(cursor)


def get_current_structures(database, args=None):
    """Returns all the structures that haven't been removed.
    """
    collection = get_structure_collection(database)
    arguments = []
    if args:
        arguments = [db_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
    arguments.append(db_utils.make_single_field_argument("remove_date", None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    return db_utils.unload_cursor(cursor)


def get_structure_by_name(database, name):
    """Returns the current structure by name.
    """
    collection = get_structure_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('name', name))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    structure_list = db_utils.unload_cursor(cursor)
    try:
        return structure_list[0]
    except IndexError:
        return None


def get_structure_by_id(database, structure_id):
    """Returns the current profile by name.
    """
    structure_id = db_utils.ensure_objectid(structure_id)
    collection = get_structure_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('_id', structure_id))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    structure_list = db_utils.unload_cursor(cursor)
    try:
        return structure_list[0]
    except IndexError:
        return None


def update_structure(database, structure, changes):
    """Updates the given structure by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_structure_collection(database)
    structure_id = db_utils.ensure_objectid(structure['_id'])
    argument = db_utils.make_single_field_argument('_id', structure_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'structure'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(db_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(db_utils.make_update_argument(change, structure[change]))
    update = db_utils.merge_update_args(updates)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_structure_by_id(database, structure_id)
    return None


if __name__ == '__main__':
    print("Please use the structure dao module as method package.")
