#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

import settings

from datasetLoader import base_loader

class DataSet(base_loader(settings=settings)):
    """
    """
    def load(self):
        """An example data loader method.
        """
        for doc in self.FILES:
            save_as = doc["save_as"]
            key = os.path.basename(save_as).replace(".", "_")
            with open(save_as, "rb") as f:                
                text = f.read().decode("utf-8")
                if "json" in key:
                    data = json.loads(text)
                elif "txt" in key:
                    data = text                
                setattr(self, key, data)
        
        
if __name__ == "__main__":
    dataset = DataSet()
    dataset.clear_data_home(dataset.NAME)
    dataset.download_specific("json")
    dataset.download_specific("txt")
    dataset.load()
    print(dataset.test1_json)
    print(dataset.test2_json)
    print(dataset.test1_txt)
    print(dataset.test2_txt)