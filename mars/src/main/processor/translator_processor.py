import mars.src.main.dao.mongo.translator_dao as translator_dao
import mars.src.main.model.translator_model as translator_model
import mars.src.main.processor.generic_processor as processor_utils
from pythoncommons import directory_utils, property_reader_utils, general_utils


def create_translator_collection(database, translators=None):
    """Creates a translator collection in mongo, adding
    the passed 1D array of translators to the new collection.
    Returns the newly created translators.
    """
    translator_dao.remove_translator_collection(database)
    created_translators = translator_dao.create_translator_collection(database, translators)
    return created_translators


def remove_translator_collection(database):
    """Completely removes the translator collection from a database.
    """
    return translator_dao.remove_translator_collection(database)


def get_translator_dictionary_from_file(translator_file):
    """Returns a translator as a dictionary from the given file.
    """
    properties = property_reader.make_dictionary(translator_file)
    properties = {key: processor_utils.adjust_property_value(properties[key])
                  for key in list(properties.keys())}
    properties['translator_file'] = translator_file
    return properties


def get_translators_from_filesystem(template):
    """Gets the translators from the filesystem for the given template.
    """
    translator_directory = template['setup']['translator_directory']
    search_dictionary = processor_utils.make_search_dictionary(translator_directory, 'translator')
    translator_files = directory_tools.get_matching_files(search_dictionary)
    translators = list(map(get_translator_dictionary_from_file, translator_files))
    return translators


def make_translators_from_filesystem_closure(database, profile=None):

    def make_translators_from_filesystem(template):
        """Retrieves all the translators for a template from a filesystem
        and adds them to the database.
        """
        template = processor_utils.get_fully_qualified_paths(database, template, profile=profile)
        translators = get_translators_from_filesystem(template)
        translator_maker = translator_model.make_translator_closure(template, utils.get_timestamp())
        translators = list(map(translator_maker, translators))
        return translators

    return make_translators_from_filesystem


def add_translators_from_filesystem(database, templates, profile=None):
    """Makes a set of translators from a set of templates, then adds the translators
    to the database in a new translator collection.
    """
    if type(templates) not in [list]:
        templates = [templates]
    translator_maker = make_translators_from_filesystem_closure(database, profile=profile)
    translators = list(map(translator_maker, templates))
    translators = utils.flatten(translators, [])
    translators = create_translator_collection(database, translators)
    translators = get_current_translators(database)
    return translators


def get_current_translators(database):
    """Returns all the current translators from a database.
    """
    translators = translator_dao.get_current_translators(database)
    return translators


def get_translator_by_name(database, name=None, template=None, template_name=None, structure_name=None):
    """Returns a specific translator for the specified name. Must also pass in
    by keyword either a complete template object OR structure name. If no template name specified,
    returns the default template of the structure.
    """
    if template:
        return translator_dao.get_translator_by_name(database, name, template['name'], template['structure'])
    elif structure_name:
        return translator_dao.get_translator_by_name(database, name, template_name, structure_name)
    else:
        return None


if __name__ == '__main__':
    print('Please use translator processor module as method package.')
