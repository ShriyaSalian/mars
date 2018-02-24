import mars.src.main.dao.mongo.record_dao as record_dao
import mars.src.main.model.record_model as record_model
import mars.src.main.processor.generic_processor as processor_utils
import mars.src.main.processor.template_processor as template_processor
from python_commons import utils, record_reader
from collections import OrderedDict


def create_record_collection(database, template, records=None):
    """Creates a new record collection in mongo, adding
    the passed 1D array of records to the new collection.
    The structure name must be specified.
    Returns the newly created records.
    """
    if type(template) in [dict, OrderedDict]:
        collection = template['collection']
    else:
        collection = template
    record_dao.remove_record_collection(database, collection)
    created_records = record_dao.create_record_collection(database, collection, records)
    return created_records


def get_record_by_id(database, template, record_id):
    """Returns the record for the specified id.
    """
    if type(template) in [dict, OrderedDict]:
        collection = template['collection']
    else:
        collection = template
    record = record_dao.get_record_by_id(database, collection, record_id)
    return record


def add_new_record(database, template, record):
    """Adds a single record to the record collection for the given template.
    Returns the inserted record.
    """
    if type(template) in [dict, OrderedDict]:
        collection = template['collection']
    else:
        collection = template
    return record_dao.add_new_record(database, collection, record)


def get_all_records_for_template(database, template):
    """Returns all the records for the given template.
    """
    if type(template) in [dict, OrderedDict]:
        collection = template['collection']
    else:
        template = template_processor.get_template_by_name(template)
        collection = template['collection']
    return record_dao.get_all_records(database, collection)


def remove_all_record_collections(database):
    """Removes all record collections from the specified database.
    """
    return


def get_records_from_filesystem(translator):
    """Retrieves records from the filesystem, based on information gathered from the
    translator.
    """
    return record_reader.get_records_from_file(translator['variables'])


def make_records_from_translator(database, translator, profile=None, parameters=None):
    """Makes records for the given translator. Accepts an optional profile to override
    the default profile, and a parameters dictionary to override parameters that are
    expected from the template that may or may not be provided by the translator.
    """
    translator = processor_utils.get_fully_qualified_paths(database, translator, profile=profile)
    template = template_processor.get_template_by_name(translator['structure'],
                                                       translator['template'])
    return template


def make_records_from_filesystem_closure(database, profile=None):
    """Closure method that accepts a profile for overwriting relative paths.
    This closure returns a method that accepts a filesystem type translator
    and returns structure records matching the translator.
    """

    def make_records_from_filesystem(translator):
        """This method gathers and adds filesystem records to the structure for the
        translator. It adds relevant information to each record that it returns, based
        on association and ability information from the template and structure.
        It returns the added records.
        """
        translator = processor_utils.get_fully_qualified_paths(database, translator, profile=profile)
        records = get_records_from_filesystem(translator)
        template = template_processor.get_template_by_name(translator['structure'],
                                                           translator['template'])
        record_maker = record_model.make_record_closure(template, translator, utils.get_timestamp())
        records = list(map(record_maker, records))
        return records

    return make_records_from_filesystem


def add_records_from_filesystem(translators, profile=None):
    """Adds a set of records for a given set of of translators, returning
    the created records.
    """
    if type(translators) not in [list]:
        translators = [translators]
    record_maker = make_records_from_filesystem_closure(profile=profile)
    records = list(map(record_maker, translators))
    records = utils.flatten(records, [])
    return records
