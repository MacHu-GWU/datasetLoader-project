#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datasetLoader.data_loader import DatasetLoader


class Dataset(object):
    def __init__(self, name, description, data):
        self.name = name
        self.description = description
        self.data = data
        

class ClusteringDataset(DatasetLoader):
    dl_dirname = "ml-datasets"
    bucket_name = "sanherabbit.com"
    s3_dirpath = "machine-learning-dataset"

    def load_P3(self):
        filename = "pathbased.txt"
        dl_path, s3_url = self.download_file(filename)
        df = pd.read_csv(dl_path, sep="\t", header=None)
        df.columns = ["x", "y", "label"]
        X = df[["x", "y"]]
        y = df["label"]
        print(X, y)
        return df

# ml_datasets.download_file("pathbased.txt")

c_dataset = ClusteringDataset()
data = c_dataset.load_P3()
print(data)


