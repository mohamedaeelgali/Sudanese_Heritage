import argparse
import os
import pickle
from random import randint
import numpy as np

import os, sys, inspect
from pathlib import Path

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp','PNG','JPG','JPEG'}


BASE_DIR = Path(__file__).resolve().parent


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,str(BASE_DIR))
from src_files import find_similar as fs
from src_files import search_catalog as sc




def visual_search(img,db,dataset):
    search = sc.search_catalog(dataset=dataset)
    return search.run(img, load_features=True, model='Inception_Resnet', data_augmentation=True,db=db) 


if __name__=='__main__':
	visual_search()

