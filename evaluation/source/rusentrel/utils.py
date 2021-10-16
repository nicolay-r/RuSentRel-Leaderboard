def iter_synonym_groups(input_file):
    """ All the synonyms groups organized in lines, where synonyms demarcated by ',' sign
    """
    for line in input_file.readlines():
        yield line.decode('utf-8').split(',')
