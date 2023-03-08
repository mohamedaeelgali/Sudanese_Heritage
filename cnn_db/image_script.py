import os
import sys
import argparse
from zipfile import ZipFile
from pathlib import Path
from django.core.files import File
from uuid import uuid4
from django.core.files.base import ContentFile
BASE_DIR_PROJECT=Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
BASE_DIR = Path(__file__).resolve().parent

import django

#from django.core.files import File


def main():

 from cnn_db.models import ClassPersonDescription,ClassPersonImage
 parser = argparse.ArgumentParser(description='Taking zip path')
 parser.add_argument('--path', dest='path')
 args = parser.parse_args()

 with ZipFile(args.path, 'r') as zipObj:

       listOfiles = zipObj.namelist() 
       for file2 in listOfiles:
             elem=file2
             split=elem.split('/')
             if not file2:
               print('not')
               continue
             if len(split)>1:
              target_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/temp'
              zimg=zipObj.extract(file2,target_dir)
              if zimg.endswith(('.png','.jpg','.jpeg')):
               print(split[0])
               p_desc_obj=ClassPersonDescription.objects.get(name=split[0])
               print('testrtt')
               ip_image=ClassPersonImage.objects.create(name=p_desc_obj)
               _, ext = os.path.splitext(zimg)
               name = f'{uuid4()}{ext}'
               #pk=p_desc_obj.pk
               ip_image.img.save(name,content=ContentFile(zimg),
            save=True
        )
              # ipo.name_id=pk
              # ipo.img(zimg, File().read())
               #ipo=ClassPersonImage(name=p_desc_obj,img=zimg)
              # ipo.save()

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cnn_web.settings'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnn_web.settings")  
    django.setup()  
    main()               