from evaluation.core.labels.str_fmt import StringLabelsFormatter
from evaluation.source.common.labels import PositiveLabel, NegativeLabel


class RuSentRelLabelsFormatter(StringLabelsFormatter):

    def __init__(self):

        stol = {"neg": NegativeLabel(),
                "pos": PositiveLabel()}

        super(RuSentRelLabelsFormatter, self).__init__(stol=stol)
