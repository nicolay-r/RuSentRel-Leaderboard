import unittest
import pandas as pd

from enum import Enum

from evaluation.core.evaluators.cmp_table import DocumentCompareTable
from evaluation.core.evaluators.modes import EvaluationModes
from evaluation.core.lemmatization.mystem import MystemWrapper
from evaluation.core.opinions.collection import OpinionCollection
from evaluation.core.synonyms import SynonymsCollection
from evaluation.core.utils import OpinionCollectionsToCompareUtils
from evaluation.evaluators.two_class import TwoClassEvaluator
from evaluation.results.two_class import TwoClassEvalResult
from evaluation.source.rusentrel.io_utils import RuSentRelVersions
from evaluation.source.rusentrel.labels_fmt import RuSentRelLabelsFormatter
from evaluation.source.rusentrel.opinions.collection import RuSentRelOpinionCollection
from evaluation.synonyms.provider import RuSentRelSynonymsCollectionProvider
from test.utils import ZippedResultsIOUtils


class ResultVersions(Enum):

    # Results with a fixed document separation.
    AttCNNFixed = "att-cnn-fixed-20e-f1-41.zip"

    # Results with cv split.
    AttPCNNCV3e40i0 = "cv3_att-pcnn_e40_i0.zip"
    AttPCNNCV3e40i1 = "cv3_att-pcnn_e40_i1.zip"
    AttPCNNCV3e40i2 = "cv3_att-pcnn_e40_i2.zip"

    SelfTestClassification = "self-rusentrel-11.zip"


# Expected F1-values for every result.
f1_rusentrel_v11_results = {
    # Extraction.
    ResultVersions.AttPCNNCV3e40i0: 0.31908777332585647,
    ResultVersions.AttPCNNCV3e40i1: 0.2930870695297444,
    ResultVersions.AttPCNNCV3e40i2: 0.2784798325065801,
    ResultVersions.AttCNNFixed: 0.299223261072169,
    # Classification.
    ResultVersions.SelfTestClassification: 1.0
}


class TestRuSentRelEvaluation(unittest.TestCase):

    __display_cmp_table = False
    __rusentrel_version = RuSentRelVersions.V11

    @staticmethod
    def __create_stemmer():
        return MystemWrapper()

    def __is_equal_results(self, v1, v2):
        print(abs(v1 - v2) < 1e-10)
        self.assertTrue(abs(v1 - v2) < 1e-10)

    def __test_core(self, res_version, synonyms=None,
                    eval_mode=EvaluationModes.Extraction,
                    check_results=True):
        assert(isinstance(res_version, ResultVersions))
        assert(isinstance(synonyms, SynonymsCollection) or synonyms is None)
        assert(isinstance(eval_mode, EvaluationModes))
        assert(isinstance(check_results, bool))

        # Initializing synonyms collection.
        if synonyms is None:
            # This is a default collection which we used
            # to provide the results in `f1_rusentrel_v11_results`.
            stemmer = self.__create_stemmer()
            actual_synonyms = RuSentRelSynonymsCollectionProvider.load_collection(stemmer=stemmer,
                                                                                  version=self.__rusentrel_version)
        else:
            actual_synonyms = synonyms

        # Setup an experiment labels formatter.
        labels_formatter = RuSentRelLabelsFormatter()

        # Iter cmp opinions.
        cmp_pairs_iter = OpinionCollectionsToCompareUtils.iter_comparable_collections(
            doc_ids=ZippedResultsIOUtils.iter_doc_ids(filepath_or_version=res_version),
            read_etalon_collection_func=lambda doc_id: OpinionCollection(
                opinions=RuSentRelOpinionCollection.iter_opinions_from_doc(
                    doc_id=doc_id,
                    labels_fmt=labels_formatter),
                synonyms=actual_synonyms,
                error_on_duplicates=False,
                error_on_synonym_end_missed=True),
            read_result_collection_func=lambda doc_id: OpinionCollection(
                opinions=ZippedResultsIOUtils.iter_doc_opinions(
                    doc_id=doc_id,
                    filepath_or_version=res_version,
                    labels_formatter=labels_formatter),
                synonyms=actual_synonyms,
                error_on_duplicates=False,
                error_on_synonym_end_missed=False))

        # getting evaluator.
        evaluator = TwoClassEvaluator(eval_mode=eval_mode)

        # evaluate every document.
        result = evaluator.evaluate(cmp_pairs=cmp_pairs_iter)
        assert(isinstance(result, TwoClassEvalResult))

        # calculate results.
        result.calculate()

        # logging all the result information.
        for doc_id, doc_info in result.iter_document_results():
            print("{}:\t{}".format(doc_id, doc_info))
        print("------------------------")
        print(str(result.TotalResult))
        print("------------------------")

        # Display cmp tables (optionally).
        if self.__display_cmp_table:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                for doc_id, df_cmp_table in result.iter_dataframe_cmp_tables():
                    assert(isinstance(df_cmp_table, DocumentCompareTable))
                    print("{}:\t{}\n".format(doc_id, df_cmp_table.DataframeTable))
            print("------------------------")

        if check_results:
            self.__is_equal_results(v1=result.get_result_by_metric(TwoClassEvalResult.C_F1),
                                    v2=f1_rusentrel_v11_results[res_version])

    def test_ann_cnn(self):
        self.__test_core(ResultVersions.AttCNNFixed)

    def test_ann_pcnn_cv(self):
        self.__test_core(ResultVersions.AttPCNNCV3e40i0)
        self.__test_core(ResultVersions.AttPCNNCV3e40i1)
        self.__test_core(ResultVersions.AttPCNNCV3e40i2)

    def test_classification(self):
        self.__test_core(ResultVersions.SelfTestClassification,
                         eval_mode=EvaluationModes.Classification)


if __name__ == '__main__':
    unittest.main()
