from pythoncommons import mongo_utils, general_utils


def get_group_collection(database):
    """Connects to the database and returns a pointer
    to the groups collection.
    """
    connection = mongo_utils.mongo_get_connection(database)
    collection = mongo_utils.mongo_get_collection(connection, "mars_groups")
    return collection


def add_group(database, group):
    """Adds a single group to the groups collection for the given database.
    """
    collection = get_group_collection(database)
    group_id = mongo_utils.mongo_insert_one(collection, group)
    return get_group_by_id(database, group_id)


def create_group_collection(database, groups):
    """Inserts all the given groups into the groups collection.
    Will automatically create the groups collection if it does not exist.
    Returns the groups in the collection.
    """
    collection = get_group_collection(database)
    record_ids = mongo_utils.mongo_insert_many(collection, groups)
    return record_ids


def remove_group_collection(database):
    """Completely blows away the group collection.
    """
    collection = get_group_collection(database)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_all_groups(database, args=None):
    """Returns all the groups in storage.
    """
    collection = get_group_collection(database)
    if args:
        arguments = [mongo_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
        argument = utils.merge_list_of_dicts(arguments)
        cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    else:
        cursor = mongo_utils.mongo_find_records(collection)
    return mongo_utils.unload_cursor(cursor)


def get_current_groups(database, args=None):
    """Returns all the groups that haven't been removed.
    """
    collection = get_group_collection(database)
    arguments = []
    if args:
        arguments = [mongo_utils.make_single_field_argument(arg['key'], arg['value'], arg_type=arg['operation']) for arg in args]
    arguments.append(mongo_utils.make_single_field_argument("remove_date", None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    return mongo_utils.unload_cursor(cursor)


def get_group_by_name(database, name):
    """Returns the current group by name.
    """
    collection = get_group_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    group_list = mongo_utils.unload_cursor(cursor)
    try:
        return group_list[0]
    except IndexError:
        return None


def get_group_by_id(database, group_id):
    """Returns the current group by id.
    """
    group_id = mongo_utils.ensure_objectid(group_id)
    collection = get_group_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('_id', group_id))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    group_list = mongo_utils.unload_cursor(cursor)
    try:
        return group_list[0]
    except IndexError:
        return None


def update_group(database, group, changes):
    """Updates the given group by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_group_collection(database)
    group_id = mongo_utils.ensure_objectid(group['_id'])
    argument = mongo_utils.make_single_field_argument('_id', group_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'group'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(mongo_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(mongo_utils.make_update_argument(change, group[change]))
    update = mongo_utils.merge_update_args(updates)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_group_by_id(database, group_id)
    return None


if __name__ == '__main__':
    print("Please use the structure dao module as method package.")
