from evaluation.core.labels.str_fmt import StringLabelsFormatter
from evaluation.source.rusentrel.const import POS_LABEL_STR, NEG_LABEL_STR
from evaluation.source.rusentrel.io_utils import RuSentRelVersions, RuSentRelIOUtils
from evaluation.source.rusentrel.labels_fmt import RuSentRelLabelsFormatter
from evaluation.source.rusentrel.opinions.formatter import RuSentRelOpinionCollectionFormatter


class RuSentRelOpinionCollection:
    """
    Collection of sentiment opinions between entities
    """

    @staticmethod
    def iter_opinions_from_doc(doc_id,
                               labels_fmt=RuSentRelLabelsFormatter(),
                               version=RuSentRelVersions.V11):
        """
        doc_id:
        synonyms: None or SynonymsCollection
            None corresponds to the related synonym collection from RuSentRel collection.
        version:
        """
        assert(isinstance(version, RuSentRelVersions))
        assert(isinstance(labels_fmt, StringLabelsFormatter))
        assert(labels_fmt.supports_value(POS_LABEL_STR))
        assert(labels_fmt.supports_value(NEG_LABEL_STR))

        return RuSentRelIOUtils.iter_from_zip(
            inner_path=RuSentRelIOUtils.get_sentiment_opin_filepath(doc_id),
            process_func=lambda input_file: RuSentRelOpinionCollectionFormatter._iter_opinions_from_file(
                input_file=input_file,
                labels_formatter=labels_fmt,
                error_on_non_supported=True),
            version=version)
