#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join

NAME = "datasetLoader-dataset"
SERVER = "https://s3.amazonaws.com/eni.e5/e5SanheDataScience/wbh-dataset/datasetLoader"
FILES = [
    {"file": join("json", "test1.json"), "md5": "c67583e8bd8c85b7efe0fd4ed78a2a62"},
    {"file": join("json", "test2.json"), "md5": "d8fe349584c3c1b18393e235796a5acb"},
    {"file": join("txt", "test1.txt"), "md5": "ed076287532e86365e841e92bfc50d8c"},
    {"file": join("txt", "test2.txt"), "md5": "f9e86f7640789b763a16049e1ec87715"},
]