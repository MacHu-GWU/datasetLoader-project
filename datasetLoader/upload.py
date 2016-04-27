#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

本脚本可供dataset的开发者使用。用于打印setting.py文件中FILES一项的内容。
"""

from __future__ import print_function

import os
from datasetLoader import DatasetLoader

    
def print_files(dir_path):
    """After preparing your dataset, call this function, and add file
    information to your setting.py file!
    
    :param dir_path: your data home abspath.
    """
    lines = list()
    lines.append("FILES = [")
    for current_dir, folder_list, fname_list in os.walk(dir_path):
        for fname in fname_list:
            abspath = os.path.join(current_dir, fname)
            md5 = DatasetLoader.md5_of_file(abspath)
            relpath = os.path.relpath(abspath, dir_path)
            chunks = relpath.split(os.sep)
            line = '    {"file": join("%s"), "md5": "%s"},' % ('", "'.join(chunks), md5)
            lines.append(line)
    lines.append("]")
    print("\n".join(lines))
    
if __name__ == "__main__":
    print_files("testdata")