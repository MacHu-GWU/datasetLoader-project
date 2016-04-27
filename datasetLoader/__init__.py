#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

用S3来Host你的测试数据, 供大家下载或程序调用, 在现在成为了一个非常流行的方案。
而为dataset的download, loading专门写一个类, 并组织你本地的文件系统和S3上的
文件系统是一件很琐碎的事情。datasetLoader可以通过使用继承, 快速地帮你创建一个
dataset类, 而你只需要专注于设计你的数据结构, 和数据读取方式。而文件的自动下载
和文件系统的结构设计, 就交给datasetLoader来做就好了。
"""

__version__ = "0.0.1"
__short_description__ = "A dataset loader class quick builder"
__author__ = "Sanhe Hu"


import os, shutil
import logging
import hashlib

import requests


logger = logging.getLogger("datasetLoader")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class DatasetLoader(object):
    r"""
    
    Local data directory
    
    - Windows: ``C:\Users\<user-name>\<dataset-name>``
    - MacOS: ``/Users/<user-name>/<dataset-name>``
    - Linux: ``/home/<user-name>/<dataset-name>``
    
    Bascially, your project file structure is like this::
        
        username = admin
        
        from os.path import join
        
        NAME = datasetLoader-dataset
        SERVER = https://s3.amazonaws.com/bucket-name/datasetLoader-dataset
        FILES = [
            {"file": join("json", "test1.json"), "md5": "c67583e8bd8c85b7efe0fd4ed78a2a62"},
            {"file": join("json", "test2.json"), "md5": "d8fe349584c3c1b18393e235796a5acb"},
            {"file": join("txt", "test1.txt"), "md5": "ed076287532e86365e841e92bfc50d8c"},
            {"file": join("txt", "test2.txt"), "md5": "f9e86f7640789b763a16049e1ec87715"},
        ]

    What's on your local drive::
    
        C:\Users\admin\datasetLoader-dataset\json\test1.json
        C:\Users\admin\datasetLoader-dataset\json\test2.json
        C:\Users\admin\datasetLoader-dataset\txt\test1.txt
        C:\Users\admin\datasetLoader-dataset\txt\test1.txt
    
    What's on your S3::
    
        https://s3.amazonaws.com/bucket-name/datasetLoader-dataset/json/test1.json
        https://s3.amazonaws.com/bucket-name/datasetLoader-dataset/json/test2.json
        https://s3.amazonaws.com/bucket-name/datasetLoader-dataset/txt/test1.txt
        https://s3.amazonaws.com/bucket-name/datasetLoader-dataset/txt/test2.txt
    """
    LOGGER = logger
    #--- Data Home ---
    @staticmethod
    def get_data_home(data_home):
        """Return the path of the dataset dir.
        """
        data_home = os.path.join(os.path.expanduser("~"), data_home)
        if not os.path.exists(data_home):
            os.makedirs(data_home)
        return data_home
    
    def clear_data_home(self, data_home):
        """Delete all the content of the data home cache."""
        data_home = self.get_data_home(data_home)
        shutil.rmtree(data_home)
        
    #--- Download Method ---
    @staticmethod
    def md5_of_file(abspath):
        """Calculate md5 value of a file.
        """
        chunksize = 1024 ** 2
        m = hashlib.md5()
        with open(abspath, "rb") as f:
            while True:
                data = f.read(chunksize)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()
    
    def download_url(self, url, save_as, md5=None):
        """Download binary from url to local drive. If md5 value is given,
        existing file will be overwrite anyway if md5 doesn't match.
        """
        self.LOGGER.info("Download '%s' from %s ..." % (save_as, url))
        if os.path.exists(save_as): # exists, check md5
            if self.md5_of_file(save_as) == md5:
                self.LOGGER.info("    '%s' is already downloaded." % save_as)
                return
            else:
                self.LOGGER.info("    '%s' already exists, "
                                 "but md5 is incorrect" % save_as)
        
        try:
            dirname, basename = os.path.split(save_as)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
                
            with open(save_as, "wb") as f:
                f.write(requests.get(url).content)
            self.LOGGER.info("    Complete!")
            
        except:
            self.LOGGER.info("    Failed!")

    def download_specific(self, keyword):
        """Only download data file having the 'keyword'.
        """
        if not keyword:
            return
        
        for doc in self.FILES:
            if keyword not in doc["file"]:
                continue
            
            url = self.SERVER + doc["file"].replace("\\", "/")
            save_as = doc["save_as"]
            md5 = doc["md5"]
            self.download_url(url, save_as, md5)
            
    def download_all(self):
        """Download all data file to data home.
        """
        for doc in self.FILES:
            url = self.SERVER + doc["file"].replace("\\", "/")
            save_as = doc["save_as"]
            md5 = doc["md5"]            
            self.download_url(url, save_as, md5)

    #--- Load Method ---
    def load(self):
        """Override .load() to customize your data loader.
        """
        self.LOGGER.info("Override .load() to customize your data loader.")


def base_loader(settings):
    """DatasetLoader base class constructor method.
    """
    for attr in dir(settings):
        if attr.isupper():
            setattr(DatasetLoader, attr, getattr(settings, attr))
            
    if not DatasetLoader.SERVER.endswith("/"):
        DatasetLoader.SERVER = DatasetLoader.SERVER + "/"
        
    for doc in DatasetLoader.FILES:
        doc["save_as"] = os.path.join(
            DatasetLoader.get_data_home(DatasetLoader.NAME), doc["file"])
    return DatasetLoader