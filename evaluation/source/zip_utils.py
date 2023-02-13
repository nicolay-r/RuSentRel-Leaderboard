from . import utils
import zipfile

import enum


class ZipArchiveUtils(object):

    @staticmethod
    def get_archive_filepath(data):
        raise NotImplementedError()

    @classmethod
    def iter_from_zip(cls, inner_path, process_func, zip_filepath_data):
        assert(isinstance(inner_path, str))
        assert(callable(process_func))

        with zipfile.ZipFile(cls.get_archive_filepath(zip_filepath_data), "r") as zip_ref:
            with zip_ref.open(inner_path, mode='r') as c_file:
                for result in process_func(c_file):
                    yield result

    @classmethod
    def iter_filenames_from_zip(cls, zip_filepath_data):
        with zipfile.ZipFile(cls.get_archive_filepath(zip_filepath_data), "r") as zip_ref:
            return iter(zip_ref.namelist())

    @staticmethod
    def get_data_root():
        return utils.get_default_download_dir()
