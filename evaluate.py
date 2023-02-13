import argparse

from tqdm import tqdm

from evaluation.core.evaluators.modes import EvaluationModes
from evaluation.core.lemmatization.mystem import MystemWrapper
from evaluation.core.opinions.collection import OpinionCollection
from evaluation.core.utils import OpinionCollectionsToCompareUtils
from evaluation.evaluators.two_class import TwoClassEvaluator
from evaluation.results.two_class import TwoClassEvalResult
from evaluation.source.rusentrel.io_utils import RuSentRelVersions
from evaluation.source.rusentrel.labels_fmt import RuSentRelLabelsFormatter
from evaluation.source.rusentrel.opinions.collection import RuSentRelOpinionCollection
from evaluation.synonyms.provider import RuSentRelSynonymsCollectionProvider
from test.utils import ZippedResultsIOUtils


if __name__ == '__main__':

    # Setup parser.
    parser = argparse.ArgumentParser(description="Submission evaluation for RuSentRel dataset.")

    parser.add_argument('--input', dest='input', type=str, default=None, help='Input file')
    parser.add_argument('--mode', dest='eval_mode', type=str, default="extraction",
                        choices=['extraction', 'classification'],
                        help='Input file')

    # Parsing arguments.
    args = parser.parse_args()

    stemmer = MystemWrapper()
    actual_synonyms = RuSentRelSynonymsCollectionProvider.load_collection(stemmer=stemmer,
                                                                          version=RuSentRelVersions.V11)

    results = args.input

    eval_mode = EvaluationModes.Extraction if args.eval_mode == 'extraction' else EvaluationModes.Classification

    # Setup an experiment labels formatter.
    labels_formatter = RuSentRelLabelsFormatter()

    # Iter cmp opinions.
    cmp_pairs_iter = OpinionCollectionsToCompareUtils.iter_comparable_collections(
        doc_ids=tqdm(ZippedResultsIOUtils.iter_doc_ids(filepath_or_version=results)),
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
                filepath_or_version=results,
                labels_formatter=labels_formatter),
            synonyms=actual_synonyms,
            error_on_duplicates=False,
            error_on_synonym_end_missed=False))

    # getting evaluator.
    evaluator = TwoClassEvaluator(eval_mode=eval_mode)

    # evaluate every document.
    result = evaluator.evaluate(cmp_pairs=cmp_pairs_iter)
    assert (isinstance(result, TwoClassEvalResult))

    # calculate results.
    result.calculate()

    # logging all the result information.
    for doc_id, doc_info in result.iter_document_results():
        print("{}:\t{}".format(doc_id, doc_info))

    print("------------------------")
    print(str(result.TotalResult))
    print("------------------------")