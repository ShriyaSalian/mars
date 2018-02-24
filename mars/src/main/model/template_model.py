from python_commons import utils
from copy import deepcopy
from collections import OrderedDict
import mars.src.main.model.generic_model as generic_model


def get_field_type(structure, template):
    """Creates and returns a field type using the given template
    and structures. (Structure.template)
    """
    if type(structure) in [dict, OrderedDict]:
        struct_type = structure['name']
    else:
        struct_type = structure
    if type(template) in [dict, OrderedDict]:
        template_type = template['name']
    else:
        template_type = template
    return struct_type + '.' + template_type


def get_field_type_collection(field_type):
    """Returns the collection version of the given field type.
    """
    collection_type = 'collection({0})'.format(field_type)
    return collection_type


def set_template_name(template, name):
    """Sets a templates name to the given name and returns the updated template.
    """
    template['name'] = name
    return template


def set_template_structure(template, structure):
    """Sets a templates structure to the given structure and returns the updated template.
    """
    template['structure'] = structure
    return template


def remove_fields_by_type(template, field_type):
    """Removes any field that is of the given field type from the given field.
    """
    field_types = [field_type, get_field_type_collection(field_type)]
    template['fields'] = [field for field in template['fields'] if field['type'] not in field_types]
    return template


def get_new_field(field_name, field_type, required=False, default=None, others=None):
    """Returns a basic field for attachment on a template.
    """
    field = {}
    field['name'] = field_name
    field['type'] = field_type
    field['required'] = required
    field['default'] = default
    if others:
        for key in list(others.keys()):
            field[key] = others[key]
    return field


def copy_fields(template):
    fields = template['fields']
    return deepcopy(fields)


def update_remove_date(template, remove_date=utils.get_timestamp()):
    """Sets the remove date for a given template, returning the updated template.
    """
    template['remove_date'] = str(remove_date)
    return template


def adjust_template_collection(template):
    """Method used to build a unique collection name and add it to the template
    dictionary. Returns the updated template.
    """
    unique_collection = 'mars_' + utils.get_random_string(numbers=True, length=8)
    template['collection'] = unique_collection
    return template


def make_template_closure(structure, add_date=utils.get_timestamp(), setup=True):
    """Closure function returning the function that creates a structure template.
    """

    field_translator_dictionary = {}
    field_translator_dictionary['field_names'] = 'name'
    field_translator_dictionary['field_types'] = 'type'
    field_translator_dictionary['field_required'] = 'required'
    field_translator_dictionary['field_defaults'] = 'default'

    index_translator_dictionary = {}
    index_translator_dictionary['index_fields'] = 'field'
    index_translator_dictionary['index_types'] = 'type'

    def get_empties():
        return [None, False, 'None', 'False']

    def get_setup_keys():
        return ['translator_directory']

    def is_field_key(key):
        if key in list(field_translator_dictionary.keys()):
            return True
        return False

    def is_index_key(key):
        if key in list(index_translator_dictionary.keys()):
            return True
        return False

    def parse_template_file_name(file_name):
        return file_name.rsplit('/', 1)[-1].rsplit('.')[0]

    def make_template(template):
        add_dates(template)
        add_type(template)
        adjust_name(template)
        adjust_description(template)
        adjust_collection(template)
        adjust_structure(template)
        adjust_fields(template)
        adjust_indeces(template)
        adjust_translators(template)
        if setup:
            move_setup_properties(template)
        return template

    def add_dates(template):
        template['add_date'] = add_date
        template['remove_date'] = None
        return template

    def add_type(template):
        template['type'] = 'template'
        return template

    def adjust_name(template):
        if 'name' not in list(template.keys()):
            if 'template_file' in list(template.keys()):
                template['name'] = parse_template_file_name(template['template_file'])
            else:
                template['name'] = 'auto_' + utils.get_random_string(length=10)
        utils.remove_dictionary_keys(template, ['template_file'])
        return template

    def adjust_description(template):
        if 'description' not in list(template.keys()):
            template['description'] = ''
        return template

    def adjust_collection(template):
        if 'collection' not in list(template.keys()):
            unique_collection = 'mars_' + utils.get_random_string(numbers=True, length=10)
            template['collection'] = unique_collection
        return template

    def adjust_structure(template):
        if type(structure) in [dict, OrderedDict]:
            template['structure'] = structure['name']
        else:
            template['structure'] = structure
        return template

    def adjust_fields(template):
        if setup:
            field_properties = {key: template[key] for key in list(template.keys()) if is_field_key(key)}
            field_tool = generic_model.field_converter_closure(field_properties, field_translator_dictionary)
            field_properties = list(map(field_tool, field_properties))
            template['fields'] = list(map(generic_model.combine_fields, list(zip(*field_properties))))
            utils.remove_dictionary_keys(template, list(field_translator_dictionary.keys()))
        elif 'fields' not in list(template.keys()):
            template['fields'] = []
        return template

    def adjust_indeces(template):
        index_properties = {key: template[key] for key in list(template.keys()) if is_index_key(key)}
        field_tool = generic_model.field_converter_closure(index_properties, index_translator_dictionary)
        index_properties = list(map(field_tool, index_properties))
        template['indeces'] = list(map(generic_model.combine_fields, list(zip(*index_properties))))
        utils.remove_dictionary_keys(template, list(index_translator_dictionary.keys()))
        return template

    def adjust_translators(template):
        if 'translators' not in list(template.keys()) or not template['translators']:
            template['translators'] = []
        if type(template['translators']) in [str, str]:
            template['translators'] = [template['translators']]
        return template

    def move_setup_properties(template):
        template['setup'] = {key: template[key] for key in get_setup_keys()}
        utils.remove_dictionary_keys(template, get_setup_keys())
        return template

    return make_template
