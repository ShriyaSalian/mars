from python_commons import utils


def add_template(structure, template_name, order=None):
    """Adds a single template to the given structure.
    If the order is specified, adds the template at the specified order.
    """
    if order is not None:
        structure['templates'].insert(order, template_name)
    else:
        structure['templates'].append(template_name)
    return structure


def remove_template(structure, template_name):
    """Removes the template reference for the given structure. Returns the updated
    structure.
    """
    structure['templates'] = [template for template in structure['templates'] if template != template_name]
    return structure


def add_templates_to_structure(structure, templates):
    """Adds given templates to the structure in the order specified by the structure.
    """
    ordered_templates = []
    for template_name in structure['templates']:
        for template in templates:
            if template['name'] == template_name:
                ordered_templates.append(template)
    structure['templates'] = ordered_templates
    return structure


def make_structure_closure(add_date=utils.get_timestamp(), setup=True):

    def get_setup_keys():
        return ['template_directory']

    def make_structure(structure):
        """Prepares a structure dictionary for addition to the structure database.
        """
        add_dates(structure)
        add_type(structure)
        adjust_templates(structure)
        if setup:
            move_setup_properties(structure)
        return structure

    def add_dates(structure):
        structure['add_date'] = add_date
        structure['remove_date'] = None
        return structure

    def add_type(structure):
        structure['type'] = 'structure'
        return structure

    def adjust_templates(structure):
        if 'templates' not in list(structure.keys()) or not structure['templates']:
            structure['templates'] = []
        if type(structure['templates']) in [str, str]:
            structure['templates'] = [structure['templates']]
        return structure

    def move_setup_properties(structure):
        structure['setup'] = {key: structure[key] for key in get_setup_keys()}
        utils.remove_dictionary_keys(structure, get_setup_keys())
        return structure

    return make_structure
