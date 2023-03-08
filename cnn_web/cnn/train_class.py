import argparse
import os
import pickle
from random import randint
import django
from src_files import find_similar as fs
from src_files import search_catalog as sc
from pathlib import Path
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
BASE_DIR_PROJECT=Path(__file__).resolve().parent.parent.parent
sys.path.insert(0,str(BASE_DIR_PROJECT))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnn_web.settings'
django.setup()



parser = argparse.ArgumentParser(description='Dataset and database')

parser.add_argument('--dataset', type=str, default='pass')
parser.add_argument('--database', type=str, default='pass')
parser.add_argument('--task', type=str, default='fit')
args = parser.parse_args()

if args.dataset=='class_d':
     from Class_D_db.models import ClassTrainModel

if args.dataset=='class_c':
     from ClassCdb.models import ClassTrainModel

def fit():
    sim = fs.find_similar(dataset=args.dataset)
    sim.fit(k=5, model='Inception_Resnet', 
            data_augmentation=True, save_similar_items=False,db=args.database)

    print(ClassTrainModel.objects.filter(status='Processing').update(status='Active'))


if args.task == 'fit':
    fit()
