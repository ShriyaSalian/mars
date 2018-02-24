from python_commons import utils
import mars.src.main.model.generic_model as generic_model


def make_translator_closure(template, add_date):
    """Closure function returning the function that creates a template translator.
    """

    source_translator_dictionary = {}
    source_translator_dictionary['source_structure'] = 'structure'
    source_translator_dictionary['source_template'] = 'template'

    target_translator_dictionary = {}
    target_translator_dictionary['target_structure'] = 'structure'
    target_translator_dictionary['target_template'] = 'template'

    def is_source_key(key):
        if key in list(source_translator_dictionary.keys()):
            return True
        return False

    def is_target_key(key):
        if key in list(target_translator_dictionary.keys()):
            return True
        return False

    def get_cleanup_keys():
        return ['translator_file']

    def make_translator(translator):
        add_dates(translator)
        add_structure(translator)
        add_template(translator)
        add_source(translator)
        add_target(translator)
        add_map(translator)
        cleanup(translator)
        return translator

    def add_dates(translator):
        translator['add_date'] = add_date
        translator['remove_date'] = None
        return translator

    def add_structure(translator):
        translator['structure'] = template['structure']
        return translator

    def add_template(translator):
        translator['template'] = template['name']
        return translator

    def add_source(translator):
        source_properties = {key: translator[key] for key in list(translator.keys()) if is_source_key(key)}
        source_tool = generic_model.field_converter_closure(source_properties, source_translator_dictionary)
        source_properties = list(map(source_tool, source_properties))
        translator['source'] = list(map(generic_model.combine_fields, list(zip(*source_properties))))[0]
        utils.remove_dictionary_keys(translator, list(source_translator_dictionary.keys()))
        return translator

    def add_target(translator):
        target_properties = {key: translator[key] for key in list(translator.keys()) if is_target_key(key)}
        if target_properties:
            target_tool = generic_model.field_converter_closure(target_properties, target_translator_dictionary)
            target_properties = list(map(target_tool, target_properties))
            translator['target'] = list(map(generic_model.combine_fields, list(zip(*target_properties))))[0]
            utils.remove_dictionary_keys(translator, list(target_translator_dictionary.keys()))
        else:
            translator['target'] = {}
            translator['target']['structure'] = template['structure']
            translator['target']['template'] = template['name']
        return translator

    def add_map(translator):
        map_fields = [key for key in list(translator.keys()) if key.startswith('Target')]
        translator['map'] = {replace_dots(field): replace_dots(translator[field]) for field in map_fields}
        utils.remove_dictionary_keys(translator, map_fields)
        return translator

    def replace_dots(field):
        if type(field) in [str, str]:
            return field.replace('.', '@')
        else:
            return [element.replace('.', '@') for element in field]

    def cleanup(translator):
        utils.remove_dictionary_keys(translator, get_cleanup_keys())
        return translator

    return make_translator
