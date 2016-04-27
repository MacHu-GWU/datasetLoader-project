#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\datasetLoader")
except Exception as e:
    print(e)
     
docfly = Docfly("datasetLoader", dst="source", 
    ignore=[
        "datasetLoader.zzz_manual_install.py",
    ]
)
docfly.fly()
