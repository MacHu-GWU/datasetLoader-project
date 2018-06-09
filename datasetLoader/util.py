#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import shutil
import hashlib
import requests
from pathlib_mate import Path


def join_all(domain, *parts):
    """
    Join all url components.

    Example::
        >>> join_all("https://www.apple.com", "iphone")
        https://www.apple.com/iphone

    :param domain: Domain parts, example: https://www.python.org
    :param parts: Other parts, example: "/doc", "/py27"
    :return: url
    """
    l = list()

    if domain.endswith("/"):
        domain = domain[:-1]
    l.append(domain)

    for part in parts:
        for i in part.split("/"):
            if i.strip():
                l.append(i)
    url = "/".join(l)
    return url


def get_data_home(data_home):
    """
    Return the path of the dataset dir.
    """
    data_home = os.path.join(os.path.expanduser("~"), data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    return data_home


def clear_data_home(data_home):
    """
    Delete all the content of the data home cache.
    """
    data_home = get_data_home(data_home)
    shutil.rmtree(data_home)


def md5_of_file(abspath):
    """
    Calculate md5 value of a file.
    """
    chunksize = 1024 ** 2  # 1MB
    m = hashlib.md5()
    with open(abspath, "rb") as f:
        while True:
            data = f.read(chunksize)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def download(url, dst, headers=None, timeout=None, wait_time=None, **kwargs):
    """
    Download binary content to destination.
    :param url: binary content url
    :param dst: path to the 'save_as' file
    :param timeout: time out time in second
    :param wait: wait time before downloading
    """
    if wait_time:  # pragma: no cover
        time.sleep(wait_time)

    response = requests.get(
        url,
        headers=headers,
        timeout=timeout,
        stream=True,
        **kwargs
    )

    chunk_size = 1024 * 1024
    downloaded_size = 0

    with open(dst, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if not chunk:  # pragma: no cover
                break
            f.write(chunk)
            downloaded_size += chunk_size
