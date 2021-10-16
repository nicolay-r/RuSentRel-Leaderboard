import io

from evaluation.core.labels.str_fmt import StringLabelsFormatter
from evaluation.core.opinions.base import Opinion
from evaluation.core.opinions.collection import OpinionCollection
from evaluation.core.opinions.formatter import OpinionCollectionsFormatter


class RuSentRelOpinionCollectionFormatter(OpinionCollectionsFormatter):

    # region protected public methods

    def iter_opinions_from_file(self, filepath, labels_formatter, error_on_non_supported=True):
        """
        Important: For externaly saved collections (using save_to_file method) and related usage
        """
        assert(isinstance(filepath, str))
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        assert(isinstance(error_on_non_supported, bool))

        with open(filepath, 'r') as input_file:

            it = RuSentRelOpinionCollectionFormatter._iter_opinions_from_file(
                input_file=input_file,
                labels_formatter=labels_formatter,
                error_on_non_supported=error_on_non_supported)

            for opinion in it:
                yield opinion

    def save_to_file(self, collection, filepath, labels_formatter, error_on_non_supported=True):
        assert(isinstance(collection, OpinionCollection))
        assert(isinstance(filepath, str))
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        assert(isinstance(error_on_non_supported, bool))

        def __opinion_key(opinion):
            assert(isinstance(opinion, Opinion))
            return opinion.SourceValue + opinion.TargetValue

        sorted_ops = sorted(collection, key=__opinion_key)

        with io.open(filepath, 'w') as f:
            for o in sorted_ops:

                str_value = RuSentRelOpinionCollectionFormatter.__try_opinion_to_str(
                    opinion=o,
                    labels_formatter=labels_formatter)

                if str_value is None:
                    if error_on_non_supported:
                        raise Exception("Opinion label `{label}` is not supported by formatter".format(
                            label=o.Sentiment))
                    else:
                        continue

                f.write(str_value)
                f.write('\n')

    def save_to_archive(self, collections_iter, labels_formatter):
        raise NotImplementedError()

    # endregion

    @staticmethod
    def _iter_opinions_from_file(input_file, labels_formatter, error_on_non_supported):
        assert(isinstance(labels_formatter, StringLabelsFormatter))
        assert(isinstance(error_on_non_supported, bool))

        for line in input_file.readlines():

            line = line.decode('utf-8')

            if line == '\n':
                continue

            str_opinion = RuSentRelOpinionCollectionFormatter.__try_str_to_opinion(
                line=line,
                labels_formatter=labels_formatter)

            if str_opinion is None:
                if error_on_non_supported:
                    raise Exception("Line '{line}' has non supported label")
                else:
                    continue

            yield str_opinion

    # region private methods

    @staticmethod
    def __try_str_to_opinion(line, labels_formatter):
        args = line.strip().split(',')
        assert (len(args) >= 3)

        source_value = args[0].strip()
        target_value = args[1].strip()
        str_label = args[2].strip()

        if not labels_formatter.supports_value(str_label):
            return None

        return Opinion(source_value=source_value,
                       target_value=target_value,
                       sentiment=labels_formatter.str_to_label(str_label))

    @staticmethod
    def __try_opinion_to_str(opinion, labels_formatter):
        assert(isinstance(opinion, Opinion))
        assert(isinstance(labels_formatter, StringLabelsFormatter))

        label = opinion.Sentiment

        if not labels_formatter.supports_label(label):
            return None

        return "{}, {}, {}, current".format(
            opinion.SourceValue,
            opinion.TargetValue,
            labels_formatter.label_to_str(opinion.Sentiment))

    # endregion
