def make_record_closure(template, translator, add_date):
    """The closure function for making a standard record. Uses a translator and
    an template.
    """

    def make_record(record):
        add_dates(record)
        add_setup(record)
        add_abilities(record)
        return dict(record)

    def add_dates(record):
        record['add_date'] = add_date
        record['remove_date'] = None
        return record

    def add_setup(record):
        record['setup'] = {}
        add_translator(record)
        add_template(record)
        add_structure(record)
        return record

    def add_translator(record):
        record['setup']['translator'] = translator['name']
        return record

    def add_template(record):
        record['setup']['template'] = template['name']
        return record

    def add_structure(record):
        record['setup']['structure'] = template['structure']

    def add_abilities(record):
        record['abilities'] = {}
        if template['abilities']:
            for ability in list(template['abilities'].keys()):
                record['abilities'][ability] = {}

    return make_record
