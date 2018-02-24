from collections import OrderedDict
import re


def field_converter_closure(field_properties, translator_dictionary):

    def field_converter(field):
        if type(field_properties[field]) in [list]:
            return [{translator_dictionary[field]: field_properties[field][i]}
                    for i in range(len(field_properties[field]))]
        else:
            return [{translator_dictionary[field]: field_properties[field]}]

    return field_converter


def combine_fields(field_tuple):
    field_dictionary = {}
    for field in field_tuple:
        for key in field:
            field_dictionary[key] = field[key]
    return field_dictionary


def replace_keywords_closure(profile, replace=True):
    """Closure for the function which adds the passed profile
    to each passed dictionary as a new key called keywords.
    If replace is true, automatically does the replacement of keywords on the
    dictionary keys.
    """
    def replace_keywords(dictionary):
        dictionary = {key: replace_value(dictionary[key]) for key in list(dictionary.keys())}
        return dictionary

    def replace_value(value, pattern=['{', '}']):
        if (type(value) in [str, str]):
            if pattern == ['{', '}']:
                keywords = re.findall(r'{([^{}]*)}', value)
            if keywords:
                keyword = keywords[0]
                value = replace_keyword(value, keyword)
                replace_value(value)
        elif type(value) in [dict, OrderedDict]:
            value = replace_keywords(value)
        return value

    def replace_keyword(value, keyword, pattern=['{', '}']):
        return value.replace(pattern[0] + keyword + pattern[1], profile[keyword])

    return replace_keywords
