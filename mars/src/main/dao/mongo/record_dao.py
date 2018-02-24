from python_commons import db_utils


def get_record_collection(database, collection):
    """Connects to the database and returns a pointer
    to the record collection.
    """
    connection = db_utils.mongo_get_connection(database)
    collection = db_utils.mongo_get_collection(connection, collection)
    return collection


def create_record_collection(database, collection, records=None):
    """Inserts all the given records into the records collection for the given structure.
    Will automatically create the records collection if it does not exist.
    Returns the records in the collection.
    """
    collection = get_record_collection(database, collection)
    if records:
        record_ids = db_utils.mongo_insert_many(collection, records)
        return record_ids
    return collection


def add_new_record(database, template, record):
    """Inserts a new record into the specified database/collection, returning
    the inserted record.
    """
    collection = get_record_collection(database, template)
    record_id = db_utils.mongo_insert_one(collection, record)
    return get_record_by_id(database, template, record_id)


def get_record_by_id(database, collection, record_id):
    """Returns the record for the given id.
    """
    collection = get_record_collection(database, collection)
    argument = db_utils.make_single_field_argument('_id', record_id)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    record_list = db_utils.unload_cursor(cursor)
    try:
        return record_list[0]
    except IndexError:
        return None


def remove_record_collection(database, collection):
    """Completely blows away the record collection for a given structure.
    """
    collection = get_record_collection(database, collection)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_current_records(database, structure):
    """Returns all the records that haven't been removed for a given structure.
    """
    collection = get_record_collection(database, structure)
    argument = db_utils.make_single_field_argument("remove_date", None)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    return db_utils.unload_cursor(cursor)


def get_all_records(database, collection):
    """Returns all the records in storage for the given structure.
    """
    collection = get_record_collection(database, collection)
    cursor = db_utils.mongo_find_records(collection)
    return db_utils.unload_cursor(cursor)
