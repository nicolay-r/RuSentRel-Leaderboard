from . import utils
from os.path import join


def download():
    root_dir = utils.get_default_download_dir()

    data = {
        "rusentrel-v1_1.zip": "https://www.dropbox.com/s/6aw5jv84jf5hrl2/rusentrel-v1_1.zip?dl=1",
    }

    # Perform downloading ...
    for local_name, url_link in data.items():
        utils.download(dest_file_path=join(root_dir, local_name),
                       source_url=url_link)
