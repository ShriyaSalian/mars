from python_commons import db_utils, utils


def get_template_collection(database):
    """Connects to the database and returns a pointer
    to the templates collection.
    """
    connection = db_utils.mongo_get_connection(database)
    collection = db_utils.mongo_get_collection(connection, "mars_templates")
    return collection


def add_template(database, template):
    """Adds a single template to the template collection for the given database.
    """
    collection = get_template_collection(database)
    template_id = db_utils.mongo_insert_one(collection, template)
    return get_template_by_id(database, template_id)


def create_template_collection(database, templates):
    """Inserts all the given templates into the templates collection.
    Will automatically create the templates collection if it does not exist.
    Returns the templates in the collection.
    """
    collection = get_template_collection(database)
    record_ids = db_utils.mongo_insert_many(collection, templates)
    return record_ids


def remove_template_collection(database):
    """Completely blows away the template collection.
    """
    collection = get_template_collection(database)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_all_templates(database):
    """Returns all the templates in storage.
    """
    collection = get_template_collection(database)
    cursor = db_utils.mongo_find_records(collection)
    return db_utils.unload_cursor(cursor)


def get_all_templates_by_structure_name(database, structure_name):
    """Returns all templates in storage for the given structure name.
    """
    collection = get_template_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('structure', structure_name))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    template_list = db_utils.unload_cursor(cursor)
    try:
        return template_list
    except IndexError:
        return None


def get_current_templates_by_structure_name(database, structure_name):
    """Returns all templates in storage for the given structure name.
    """
    collection = get_template_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('structure', structure_name))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    template_list = db_utils.unload_cursor(cursor)
    try:
        return template_list
    except IndexError:
        return None


def get_current_templates(database):
    """Returns all the templates that haven't been removed.
    """
    collection = get_template_collection(database)
    argument = db_utils.make_single_field_argument("remove_date", None)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    return db_utils.unload_cursor(cursor)


def get_template_by_name(database, structure, name):
    """Returns the current template by name.
    """
    collection = get_template_collection(database)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('structure', structure))
    arguments.append(db_utils.make_single_field_argument('name', name))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    template_list = db_utils.unload_cursor(cursor)
    try:
        return template_list[0]
    except IndexError:
        return None


def get_template_by_id(database, template_id):
    """Returns the template by id.
    """
    collection = get_template_collection(database)
    template_id = db_utils.ensure_objectid(template_id)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('_id', template_id))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument)
    template_list = db_utils.unload_cursor(cursor)
    try:
        return template_list[0]
    except IndexError:
        return None


def remove_template(database, template):
    """Removes the given template from the template collection in the given database.
    """
    collection = get_template_collection(database)
    template_id = db_utils.ensure_objectid(template['_id'])
    arguments = []
    arguments.append(db_utils.make_single_field_argument('_id', template_id))
    argument = utils.merge_list_of_dicts(arguments)
    result = db_utils.mongo_remove_one(collection, argument)
    return result


def update_template(database, template, changes):
    """Updates the given template by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_template_collection(database)
    template_id = db_utils.ensure_objectid(template['_id'])
    argument = db_utils.make_single_field_argument('_id', template_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'template'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(db_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(db_utils.make_update_argument(change, template[change]))
    update = db_utils.merge_update_args(updates)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_template_by_id(database, template_id)
    return None


if __name__ == '__main__':
    print("Please use the template dao module as method package.")
