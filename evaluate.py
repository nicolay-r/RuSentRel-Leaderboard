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


def eval(actual_synonyms, results_filepath, doc_ids_filter):

    # Setup an experiment labels formatter.
    labels_formatter = RuSentRelLabelsFormatter()

    # Iter cmp opinions.
    cmp_pairs_iter = OpinionCollectionsToCompareUtils.iter_comparable_collections(
        doc_ids=tqdm(ZippedResultsIOUtils.iter_doc_ids(filepath_or_version=results_filepath,
                                                       doc_ids_filter=doc_ids_filter)),
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
                filepath_or_version=results_filepath,
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

    return result


if __name__ == '__main__':

    # Setup parser.
    parser = argparse.ArgumentParser(description="Submission evaluation for RuSentRel dataset.")

    parser.add_argument('--input', dest='input', type=str, default=None, help='Input file')
    parser.add_argument('--mode', dest='eval_mode', type=str, default="extraction",
                        choices=['extraction', 'classification'],
                        help='Input file')
    parser.add_argument('--split', dest='split', type=str, default="fixed",
                        choices=['cv3', 'fixed'])

    # Parsing arguments.
    args = parser.parse_args()

    stemmer = MystemWrapper()
    actual_synonyms = RuSentRelSynonymsCollectionProvider.load_collection(stemmer=stemmer,
                                                                          version=RuSentRelVersions.V11)

    eval_mode = EvaluationModes.Extraction if args.eval_mode == 'extraction' else EvaluationModes.Classification

    final_result = None

    # For a fixed type split.
    if args.split == 'fixed':
        result = eval(actual_synonyms=actual_synonyms,
                      results_filepath=args.input,
                      doc_ids_filter=lambda doc_id: doc_id >= 46)

        # logging all the result information.
        for doc_id, doc_info in result.iter_document_results():
            print("{}:\t{}".format(doc_id, doc_info))

        print("------------------------")
        print(str(result.TotalResult))
        print("------------------------")

    # For a cv-3 type split.
    elif args.split == 'cv3':

        cv_splits = {
            0: [2, 4, 5, 7, 8, 15, 16, 18, 19, 20, 24, 32, 35, 39, 40, 44, 48, 50, 57, 59, 64, 67, 68, 75],
            1: [3, 6, 10, 11, 12, 13, 17, 21, 27, 28, 30, 31, 34, 42, 52, 53, 54, 55, 58, 60, 62, 63, 65, 74],
            2: [1, 14, 23, 25, 29, 33, 36, 37, 38, 41, 43, 45, 46, 47, 49, 51, 56, 61, 66, 69, 71, 72, 73]
        }

        results = []
        for i in range(3):
            result = eval(actual_synonyms=actual_synonyms,
                          results_filepath=args.input,
                          doc_ids_filter=lambda doc_id: doc_id in cv_splits[i])
            print("------------------------")
            print(str(result.TotalResult))
            print("------------------------")

            results.append(result)

        print('f1:', sum([r.TotalResult['f1'] for r in results])/len(results))