from evaluation.source.rusentrel.io_utils import RuSentRelIOUtils
from evaluation.source.rusentrel.utils import iter_synonym_groups


class RuSentRelSynonymsCollectionHelper(object):

    @staticmethod
    def iter_groups(version):
        it = RuSentRelIOUtils.iter_from_zip(
            inner_path=RuSentRelIOUtils.get_synonyms_innerpath(),
            process_func=lambda input_file: iter_synonym_groups(input_file),
            version=version)

        for group in it:
            yield group
