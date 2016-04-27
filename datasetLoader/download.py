#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil

def get_data_home(data_home=None):
    """Return the path of the weatherlab dataset dir.

    This folder is used by some large dataset loaders to avoid
    downloading the data several times.

    By default the data dir is set to a folder named 'weatherlab_data'
    in the user home folder.

    Alternatively, it can be set by the 'WEATHERLAB_DATASET' environment
    variable or programmatically by giving an explit folder path. The
    '~' symbol is expanded to the user home folder.

    If the folder does not already exist, it is automatically created.
    """
    if data_home is None:
        data_home = os.environ.get(
            "DATASET", os.path.join("~", "weatherlab_dataset"))
    data_home = os.path.expanduser(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    return data_home

data_home = get_data_home()

def clear_data_home(data_home=None):
    """Delete all the content of the data home cache."""
    data_home = get_data_home(data_home)
    shutil.rmtree(data_home)


def download_dataset(filename, md5=None):
    """Weatherlab dataset downloader.
    
    **中文文档**
    
    从AWS S3上下载WeatherLab Dataset数据文件    
    """
    url = os.path.join(_s3_url, filename)
    dst = os.path.join(data_home, filename)

    if os.path.exists(dst): # exists, check md5
        if fingerprint.of_file(dst) == md5:
            logger.info("'%s' is already downloaded." % filename)
            return
    
    logger.info("Downloading '%s'..." % filename)
    download_url(url, dst, iter_size=1024**3, enable_verbose=False)
    logger.info("Complete", indent=1)
    

if __name__ == "__main__":
    print(get_data_home())