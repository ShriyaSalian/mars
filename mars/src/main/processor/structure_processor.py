import mars.src.main.dao.mongo.structure_dao as structure_dao
import mars.src.main.processor.profile_processor as profile_processor
import mars.src.main.processor.template_processor as template_processor
import mars.src.main.model.structure_model as structure_model
import mars.src.main.processor.generic_processor as processor_utils
from python_commons import directory_tools, property_reader, utils
from collections import OrderedDict


def update_structure(database, structure, changes=None):
    """Updates the structure in the given database with the passed structure.
    This will apply all the given changes passed in as a changes array keyword
    parameter (list of strings). Nested changes are permitted by using dot (.)
    notation. This will return the updated structure.
    """
    structure = structure_dao.update_structure(database, structure, changes=changes)
    return structure


def add_template_to_structure(database, structure, template, order=None):
    """Updates the given structure by adding a reference to its template to
    the structure template list. Returns the updated structure.
    """
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    if type(structure) not in [dict, OrderedDict]:
        structure = structure_dao.get_structure_by_name(database, structure)
    if type(template) in [dict, OrderedDict]:
        template = template['name']
    structure = structure_model.add_template(structure, template, order=order)
    structure = structure_dao.update_structure(database, structure, changes=['templates'])
    return structure


def remove_template_from_structure(database, structure, template):
    """Removes the reference of the given template from the given structure. Returns
    the updated structure object.
    """
    if type(structure) not in [dict, OrderedDict]:
        structure = structure_dao.get_structure_by_name(database, structure)
    if type(template) in [dict, OrderedDict]:
        template = template['name']
    structure = structure_model.remove_template(structure, template)
    structure = structure_dao.update_structure(database, structure, changes=['templates'])
    return structure


def get_structure_by_name(database, structure_name, current=True):
    """Returns the structure or structures for the given database that have the
    given name. Optionally only returns current structures (non removed structures).
    """
    if current:
        return structure_dao.get_structure_by_name(database, structure_name)
    return None


def create_structure_collection(database, structures=None):
    """Creates a structure collection in mongo, adding
    the passed 1D array of structures to the new collection.
    Returns the newly created structures.
    """
    structure_dao.remove_structure_collection(database)
    created_structures = structure_dao.create_structure_collection(database, structures)
    return created_structures


def create_new_structure(database, structure, setup=False):
    """Creates the passed structure, adding it to the dictionary.
    Optionally allows for setup keys to be included in the stored object (if stored
    from filesystem or other, for example.)
    """
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    structure_maker = structure_model.make_structure_closure(setup=setup)
    new_structure = structure_maker(structure)
    new_structure = structure_dao.add_structure(database, new_structure)
    return new_structure


def add_structure_to_database(database, structure):
    """Adds a single structure to the structure database collection.
    Returns the newly added structure.
    """
    structure = structure_dao.add_structure(database, structure)
    return structure


def remove_structure_collection(database):
    """Completely removes the structure collection from storage.
    """
    return structure_dao.remove_structure_collection(database)


def get_structure_templates_closure(database, scope):
    """Closure function for getting templates for a given structure. The closure takes
    the database and the scope as a string, which determines what subset of templates to return
    (currently supports current or all)
    """
    def get_current_structure_templates(structure):
        structure_name = structure['name']
        templates = template_processor.get_current_templates_by_structure_name(database, structure_name)
        structure = structure_model.add_templates_to_structure(structure, templates)
        return structure

    def get_all_structure_templates(structure):
        structure_name = structure['name']
        templates = template_processor.get_all_templates_by_structure_name(database, structure_name)
        structure = structure_model.add_templates_to_structure(structure, templates)
        return structure

    if scope == 'current':
        return get_current_structure_templates
    elif scope == 'all':
        return get_all_structure_templates
    return None


def get_structures_from_filesystem(structure_directory):
    """Uses the passed directory to retrieve all the structure definitions.
    Returns a list of the structure dictionary objects.
    """
    search_dictionary = processor_utils.make_search_dictionary(structure_directory, 'definition')
    structure_files = directory_tools.get_matching_files(search_dictionary)
    structures = list(map(get_structure_dictionary_from_file, structure_files))
    return structures


def add_structures_from_filesystem(database, profile=None):
    """Adds all structures in a filesystem. Uses the default profile or gets the
    profile that is specified by the user.
    """
    profile = profile_processor.get_fully_qualified_profile(database, profile)
    structure_directory = profile['structures']
    structures = get_structures_from_filesystem(structure_directory)
    structure_tool = structure_model.make_structure_closure(utils.get_timestamp())
    structures = list(map(structure_tool, structures))
    create_structure_collection(database, structures)
    structures = get_current_structures(database)
    return structures


def get_current_structures(database, args=None):
    """Returns all the current structures from a database.
    Optionally allows for an args parameter to be passed as a list of dictionary
    arguments, where each argument dictionary must have a key, value, and operation.
    E.g., [{key: group, value: worklfow, operation: not_equals}]
    """
    structures = structure_dao.get_current_structures(database, args=args)
    return structures


def get_all_structures(database, args=None):
    """Returns all the current structures from a database.
    Optionally allows for an args parameter to be passed as a list of dictionary
    arguments, where each argument dictionary must have a key, value, and operation.
    E.g., [{key: group, value: worklfow, operation: not_equals}]
    """
    structures = structure_dao.get_all_structures(database, args=args)
    return structures


def get_structure_dictionary_from_file(structure_file):
    """Returns a structure as a dictionary from the given file.
    """
    properties = property_reader.make_dictionary(structure_file)
    properties = {key: processor_utils.adjust_property_value(properties[key])
                  for key in list(properties.keys())}
    return properties

if __name__ == '__main__':
    print('Please use structure processor module as method package.')
