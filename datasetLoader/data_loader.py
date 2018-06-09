#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib_mate import Path
from . import util

S3_DOMAIN = "https://s3.amazonaws.com"


def build_dl_path(dl_dir, path):
    """
    Build download path.
    """
    return Path(dl_dir, path).abspath


def build_s3_url(bucket_name, dirpath, filename):
    """
    Build s3 url path.
    """
    return util.join_all(S3_DOMAIN, bucket_name, dirpath, filename)


class DatasetLoader(object):
    dl_dirname = None
    bucket_name = None
    s3_dirpath = None

    def __init__(self):
        self.dl_dirpath = util.get_data_home(self.dl_dirname)

    def build_dl_path(self, filename):
        return Path(self.dl_dirpath, filename).abspath

    def build_s3_url(self, filename):
        return build_s3_url(self.bucket_name, self.s3_dirpath, filename)

    def download_file(self, filename):
        dl_path = self.build_dl_path(filename)
        s3_url = self.build_s3_url(filename)
        if not Path(dl_path).exists():
            util.download(url=s3_url, dst=dl_path)
        return dl_path, s3_url

    def load_file(self, filename):
        dl_path = self.build_dl_path(filename)
        with open(dl_path, "rb") as f:
            return f.read().decode("utf-8")
