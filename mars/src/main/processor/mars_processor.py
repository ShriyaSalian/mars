import mars.src.main.processor.profile_processor as profile_processor
import mars.src.main.processor.structure_processor as structure_processor
import mars.src.main.processor.template_processor as template_processor
import mars.src.main.processor.translator_processor as translator_processor
import mars.src.main.processor.record_processor as record_processor


def remove_all_storage(database):
    """Removes all mars artifacts from storage - including profiles, structures,
    templates, translators, and records. Returns True if successful, False if not.
    """
    record_processor.remove_all_record_collections(database)
    translator_processor.remove_translator_collection(database)
    template_processor.remove_template_collection(database)
    structure_processor.remove_structure_collection(database)
    profile_processor.remove_profile_collection(database)
    return True


def basic_system_setup(database, profile=None, full_path=True, profile_name=None, profile_dictionary=None):
    """Sets up system to a basic state based on a profile, including adding
    the default profile from a full path, structures, templates, and translators.
    Does not add records. Returns the setup object now stored in database.
    """
    setup = {}
    setup['profile'] = profile_processor.add_profile_from_filesystem(database, profile=profile, full_path=full_path, profile_name=profile_name, profile_dictionary=profile_dictionary)
    setup['structures'] = structure_processor.add_structures_from_filesystem(database)
    setup['templates'] = template_processor.add_templates_from_filesystem(database, setup['structures'])
    setup['translators'] = translator_processor.add_translators_from_filesystem(database, setup['templates'])
    return setup

if __name__ == '__main__':
    print('Please use the mars processor module as method package.')
