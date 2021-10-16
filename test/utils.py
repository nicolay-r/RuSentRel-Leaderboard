from os.path import dirname, join

from evaluation.source.rusentrel.opinions.formatter import RuSentRelOpinionCollectionFormatter
from evaluation.source.zip_utils import ZipArchiveUtils


class ZippedResultsIOUtils(ZipArchiveUtils):

    @staticmethod
    def get_archive_filepath(result_version):
        return join(dirname(__file__), "data/{version}".format(version=result_version))

    @staticmethod
    def iter_doc_ids(result_version):
        for f_name in ZippedResultsIOUtils.iter_filenames_from_zip(result_version):
            doc_id_str = f_name.split('.')[0]
            yield int(doc_id_str)

    @staticmethod
    def iter_doc_opinions(doc_id, result_version, labels_formatter):
        return ZippedResultsIOUtils.iter_from_zip(
            inner_path=join("{}.opin.txt".format(doc_id)),
            process_func=lambda input_file: RuSentRelOpinionCollectionFormatter._iter_opinions_from_file(
                input_file=input_file,
                labels_formatter=labels_formatter,
                error_on_non_supported=True),
            version=result_version)
