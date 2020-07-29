import os
import re
import shutil
import sys
from pathlib import Path

import requests
import yaml
from boxsdk import OAuth2, Client


class Box(object):
    def __init__(self, developer_token):
        self._read_settings()
        self._authenticate(developer_token)

    def _read_settings(self):
        with open("config.yml", "r") as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.SafeLoader)
        self.box_client_id = cfg["box"]["client_id"]
        self.box_client_secret = cfg["box"]["client_secret"]

    def _authenticate(self, developer_token):
        # https://*.app.box.com/developers/console
        oauth2 = OAuth2(
            client_id=self.box_client_id,
            client_secret=self.box_client_secret,
            access_token=developer_token
        )
        self.box = Client(oauth2)

    def download_by_url(self, item_link, f_list, t_folder):
        dirpath = self._get_dirpath()
        # dirpath = Path(t_folder)
        print("\nDownloading to {}\n".format(dirpath))
        if not dirpath.exists():
            raise FileExistsError("{} is not reachable".format(dirpath.resolve()))
        _shared_item = self.box.get_shared_item(item_link)
        counter = 0
        if _shared_item.type == 'file' and _shared_item.name in f_list:
            # downloading single file
            print(_shared_item.name)
            with requests.get(_shared_item.get_download_url(), stream=True) as r:
                r.raise_for_status()
                with open(Path.joinpath(dirpath, _shared_item.name), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                    counter += 1

        elif _shared_item.type == 'folder':
            # downloading several files from folder
            for _file in _shared_item.get_items(limit=2000):
                if _file.name in f_list:
                    print(_file.name)
                    # with open(_file.name, 'wb') as f:
                    #     self.client.file(_file.id).download_to(f)
                    # print(_file.get_download_url())
                    with requests.get(_file.get_download_url(), stream=True) as r:
                        r.raise_for_status()
                        with open(Path.joinpath(dirpath, _file.name), 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:  # filter out keep-alive new chunks
                                    f.write(chunk)
                                    # f.flush()
                            counter += 1

        print("\nDownloaded {} out of {}".format(counter, len(f_list)))

    def _get_dirpath(self):
        dirpath = None
        if sys.platform == "win32":
            dirpath = Path('c:/', 'Users', os.getlogin(), 'Downloads')
        elif sys.platform == "linux":
            dirpath = Path('/home', os.getlogin(), 'Downloads')
        # if dirpath and dirpath.exists():
        #     shutil.rmtree(dirpath)
        #     dirpath.mkdir()
        if dirpath and not dirpath.exists():
            dirpath.mkdir()
        return dirpath
