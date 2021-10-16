from evaluation.core.lemmatization.base import Stemmer
from evaluation.source.rusentrel.io_utils import RuSentRelVersions
from evaluation.source.rusentrel.synonyms import RuSentRelSynonymsCollectionHelper
from evaluation.synonyms.collection import StemmerBasedSynonymCollection


class RuSentRelSynonymsCollectionProvider(object):

    @staticmethod
    def load_collection(stemmer, is_read_only=True, debug=False, version=RuSentRelVersions.V11):
        assert(isinstance(stemmer, Stemmer))
        return StemmerBasedSynonymCollection(
            iter_group_values_lists=RuSentRelSynonymsCollectionHelper.iter_groups(version),
            debug=debug,
            stemmer=stemmer,
            is_read_only=is_read_only)
