import mars.src.main.dao.mongo.template_dao as template_dao
import mars.src.main.model.template_model as template_model
from . import structure_processor
import mars.src.main.processor.generic_processor as processor_utils
from pythoncommons import directory_utils, property_reader_utils, general_utils
from collections import OrderedDict


def copy_template_fields(template):
    """Returns a deep copy of the template fields.
    """
    return template_model.copy_fields(template)


def create_template_collection(database, templates=None):
    """Creates an template collection in mongo, adding
    the passed 1D array of templates to the new collection.
    Returns the newly created templates.
    """
    template_dao.remove_template_collection(database)
    created_templates = template_dao.create_template_collection(database, templates)
    return created_templates


def make_template_field(field_name, field_type, required=False, default=None, others=None):
    """Creates and returns a new template field with the given name and type, optionally
    allowing the field to be specified as required, get a default, and add arbitrary
    parameters as a dictionary of key/values.
    """
    return template_model.get_new_field(field_name, field_type, required=required,
                                        default=default, others=others)


def add_template_field(database, template, field, order=None):
    """Adds the given field to the given template in the specified database.
    Optionally allows adding the field at the given location in the template field set.
    """
    pass


def remove_template_field(database, template, field):
    """Removes the given field from the given template in the specified database.
    """
    pass


def update_template_field(database, template, old_field, new_field):
    """Updates the given field within the given template in the specified database.
    """
    pass


def move_template(database, template, new_structure, new_name):
    """Moves a template from its current structure to the new structure.
    If the name is different, also updates the name.
    """
    if type(template) in [dict, OrderedDict]:
        template_id = template['_id']
        template = template_dao.get_template_by_id(database, template_id)
    else:
        template = template_dao.get_template_by_id(database, template)
    structure_processor.remove_template_from_structure(database, template['structure'], template)
    changes = []
    if template['name'] != new_name:
        template = template_model.set_template_name(template, new_name)
        changes.append('name')
    template = template_model.set_template_structure(template, new_structure)
    changes.append('structure')
    template = template_dao.update_template(database, template, changes=changes)
    structure_processor.add_template_to_structure(database, new_structure, template)
    return template


def remove_template(database, template, structure):
    """Removes the given template from the specified database.
    """
    return_dictionary = {}
    if type(template) in [dict, OrderedDict]:
        template_id = template['_id']
        template = template_dao.get_template_by_id(database, template_id)
    else:
        template = template_dao.get_template_by_id(database, template)
    removed = template_dao.remove_template(database, template)
    if removed:
        field_type = get_field_type(structure, template)
        updated_templates = remove_template_fields_by_type(database, field_type)
        updated_structure = structure_processor.remove_template_from_structure(database, structure, template)
        return_dictionary['structure'] = updated_structure
        return_dictionary['templates'] = updated_templates
    return return_dictionary


def get_field_type(structure, template):
    """Builds a field type from the given structure and template.
    """
    return template_model.get_field_type(structure, template)


def remove_fields_by_type_closure(field_type):
    """Closure for the remove_field_by_type method, which removes
    template fields by the given type (singular or collection-wise),
    returning the updated template.
    """
    def remove_fields_by_type(template):
        template = template_model.remove_fields_by_type(template, field_type)
        return template

    return remove_fields_by_type


def remove_template_fields_by_type(database, field_type):
    """Updates templates by removing any fields that match the given field_type property.
    """
    templates = template_dao.get_current_templates(database)
    field_remover = remove_fields_by_type_closure(field_type)
    templates = list(map(field_remover, templates))
    template_updater = update_template_closure(database, changes=['fields'])
    templates = list(map(template_updater, templates))
    return templates


def update_template_closure(database, changes=None):
    """A method to allow updating a group of templates for a given database
    using the same set of changes and a map pattern. Returns the updated
    database template.
    """
    def update_template(template):
        template = template_dao.update_template(database, template, changes=changes)
        return template
    return update_template


def update_template(database, template, changes=None):
    """ Updates the template with the given changes. Returns the updated template
    dictionary object.
    """
    template = template_dao.update_template(database, template, changes=changes)
    return template


def update_template_fields(database, template):
    """Updates the fields array in the given template. The given template dictionary
    object must contain the template id and the new fields array. Returns the updated
    template dictionary object.
    """
    template = template_dao.update_template(database, template, changes=['fields'])
    return template


def set_template_removal_date(database, template, remove_date):
    """Sets a removal date to the given template. Returns the updated template record.
    """
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    template = template_model.update_remove_date(template, remove_date)
    template = template_dao.update_template(database, template, changes=['remove_date'])
    return template


def create_new_template(database, structure, template, order=None, setup=False, add_date=general_utils.get_timestamp()):
    """Creates the passed template using the given structure in the given database.
    Returns the newly created template. If setup is specified as True, loads from
    a filesystem type setup.
    """
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    if type(structure) not in [dict, OrderedDict]:
        structure = structure_processor.get_structure_by_name(database, structure)
    template_maker = template_model.make_template_closure(structure, setup=setup, add_date=add_date)
    new_template = template_maker(template)
    new_template = template_dao.add_template(database, template)
    structure_processor.add_template_to_structure(database, structure, template, order=order)
    return new_template


def remove_template_collection(database):
    """Completely removes a template collection from the database.
    """
    return template_dao.remove_template_collection(database)


def get_all_templates_by_structure_name(database, structure_name):
    """Returns all the templates attached to the given structure.
    """
    return template_dao.get_all_templates_by_structure_name(database, structure_name)


def get_current_templates_by_structure_name(database, structure_name):
    """Returns all the templates attached to the given structure.
    """
    return template_dao.get_current_templates_by_structure_name(database, structure_name)


def get_template_dictionary_from_file(template_file):
    """Returns a structure as a dictionary from the given file.
    """
    properties = property_reader_utils.make_dictionary(template_file)
    properties = {key: processor_utils.adjust_property_value(properties[key])
                  for key in list(properties.keys())}
    properties['template_file'] = template_file
    return properties


def get_templates_from_filesystem(structure):
    """Gets the templates from the filesystem for the given structure.
    """
    template_directory = structure['setup']['template_directory']
    search_dictionary = processor_utils.make_search_dictionary(template_directory, 'template')
    template_files = directory_utils.get_matching_files(search_dictionary)
    templates = list(map(get_template_dictionary_from_file, template_files))
    return templates


def make_templates_from_filesystem_closure(database, profile=None):

    def make_templates_from_filesystem(structure):
        """Retrieves all the templates for a structure from a filesystem
        and adds them to the database.
        """
        structure = processor_utils.get_fully_qualified_paths(database, structure, profile=profile)
        templates = get_templates_from_filesystem(structure)
        template_maker = template_model.make_template_closure(structure, general_utils.get_timestamp())
        templates = list(map(template_maker, templates))
        return templates

    return make_templates_from_filesystem


def add_templates_from_filesystem(database, structures, profile=None):
    """Makes a set of templates from a set of structures, then adds
    the created templates to the database in a new template collection.
    """
    if type(structures) not in [list]:
        structures = [structures]
    template_maker = make_templates_from_filesystem_closure(database, profile=profile)
    templates = list(map(template_maker, structures))
    templates = general_utils.flatten(templates, [])
    templates = create_template_collection(database, templates)
    templates = get_current_templates(database)
    return templates


def get_current_templates(database):
    """Returns all the current templates from a database.
    """
    templates = template_dao.get_current_templates(database)
    return templates


def get_template_by_name(database, structure, template):
    """Returns the template with the given name for the given structure.
    """
    template = template_dao.get_template_by_name(database, structure, template)
    return template


if __name__ == '__main__':
    print('Please use template processor module as method package.')
