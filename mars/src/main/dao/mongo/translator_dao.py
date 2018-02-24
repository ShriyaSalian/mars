from python_commons import db_utils, utils


def get_translator_collection(database):
    """Connects to the database and returns a pointer
    to the translators collection.
    """
    connection = db_utils.mongo_get_connection(database)
    collection = db_utils.mongo_get_collection(connection, "mars_translators")
    return collection


def create_translator_collection(database, translators):
    """Inserts all the given translators into the translators collection.
    Will automatically create the translators collection if it does not exist.
    Returns the translators in the collection.
    """
    collection = get_translator_collection(database)
    record_ids = db_utils.mongo_insert_many(collection, translators)
    return record_ids


def remove_translator_collection(database):
    """Completely blows away the translator collection.
    """
    collection = get_translator_collection(database)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_current_translators(database):
    """Returns all the translators that haven't been removed.
    """
    collection = get_translator_collection(database)
    argument = db_utils.make_single_field_argument("remove_date", None)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    return db_utils.unload_cursor(cursor)


def get_all_translators(database):
    """Returns all the translators in storage.
    """
    collection = get_translator_collection(database)
    cursor = db_utils.mongo_find_records(collection)
    return db_utils.unload_cursor(cursor)


def get_translator_by_name(database, name, template, structure):
    """Returns the current translator by name. Must specify both an template name
    and a structure name. If no name specified, returns the default translator.
    """
    collection = get_translator_collection(database)
    arguments = []
    if not name:
        name = 'default'
    if not template:
        template = 'default'
    arguments.append(db_utils.make_single_field_argument('name', name))
    arguments.append(db_utils.make_single_field_argument('template', template))
    arguments.append(db_utils.make_single_field_argument('structure', structure))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    translator_list = db_utils.unload_cursor(cursor)
    try:
        return translator_list[0]
    except IndexError:
        return None


def get_translator_by_id(database, translator_id):
    """Returns the current translator by id.
    """
    collection = get_translator_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('_id', translator_id))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    translator_list = db_utils.unload_cursor(cursor)
    try:
        return translator_list[0]
    except IndexError:
        return None


if __name__ == '__main__':
    print("Please use the translator dao module as method package.")
