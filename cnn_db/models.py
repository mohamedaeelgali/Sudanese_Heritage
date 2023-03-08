from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import pathlib
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
import os
from pathlib import Path
from shutil import copy2,copy
from zipfile import ZipFile
from django.db import transaction
from django.dispatch import receiver
import subprocess
import sys

from uuid import uuid4
from django.core.files.base import ContentFile

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_PROJECT=Path(__file__).resolve().parent.parent

STATUS_CHOICES = [
    ('y', 'Yes'),
    ('n', 'No'),
]

class ClassPersonDescription(models.Model):
   name=models.CharField('Person name', max_length=120)
   description=models.TextField(blank=True, max_length=500)
   username=models.CharField(max_length=60,default="admin")
   approved=models.CharField('Approved',max_length=1, choices=STATUS_CHOICES, default='y')
   ip=models.CharField(max_length=50,default="None")
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)   
   def __str__(self):
      return self.name
         
class ClassPersonImage(models.Model):
   name=models.ForeignKey(ClassPersonDescription, on_delete=models.CASCADE)
   username=models.CharField(max_length=60,default="admin")
   img=models.ImageField(upload_to='class_a/')   
   approved=models.CharField('Approved',max_length=1, choices=STATUS_CHOICES, default='y')
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)
   ip=models.CharField(max_length=50,default="None")
   def __str__(self):
      return self.name.name

class ClassZipUpload(models.Model):
   comment=models.CharField('comment', max_length=120)
   zip_file=models.FileField(upload_to='zip/')
   username=models.CharField(max_length=60,default="admin")
   approved=models.CharField('Approved',max_length=1, choices=STATUS_CHOICES, default='y')
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)   
   def __str__(self):
      return self.comment

class ClassTrainModel(models.Model):
   comment=models.CharField('Comment', max_length=120)
   username=models.CharField(max_length=60,default="admin")
   status=models.CharField(max_length=60,default="Processing")
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)   
   def __str__(self):
      return self.comment      

def create_dir(sender, instance, **kwargs):
   if instance.approved=='y':
    data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/Class A/'
    dir_name=str(data_dir)+'/'+instance.name
    isdir = os.path.isdir(dir_name)
    if isdir is False:
       os.mkdir(dir_name)

def remove_dir(sender, instance, **kwargs):
   if instance.approved=='y':
    data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/Class A/'
    dir_name=str(data_dir)+'/'+instance.name
    isdir = os.path.isdir(dir_name)
    if isdir is True:
      files_in_dir = os.listdir(dir_name) 
      for file in files_in_dir: 
        os.remove(f'{dir_name}/{file}') 
      os.rmdir(dir_name)

def create_img(sender, instance, **kwargs):
   print(instance.img.name)
   print(instance.name.name)
   if instance.approved=='y':
    data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/Class A/' / instance.name.name

    img_dir=BASE_DIR_PROJECT / 'media/'
    img_dir=str(img_dir)+'/'+instance.img.name
    copy2(img_dir,data_dir)


def remove_img(sender, instance, **kwargs):
    try:
     img_dir=BASE_DIR_PROJECT / 'media/'
     img_dir=str(img_dir)+'/'+instance.img.name
     imgname_raw=instance.img.name[8:]
     os.remove(img_dir) 
     if instance.approved=='y':
    
      data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/' / instance.name.name / imgname_raw
      os.remove(data_dir) 
    except Exception as e:
     print(e) 
   

def zip_image(zpath):
   with ZipFile(zpath, 'r') as zipObj:

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
               print(p_desc_obj.pk)
               ip_image=ClassPersonImage()
               _, ext = os.path.splitext(zimg)
               fname = f'{uuid4()}{ext}'
               print(fname)
               ip_image.name=p_desc_obj
               name_dest='media/class_a/'+fname
               dst_Src=BASE_DIR_PROJECT / name_dest
               copy(zimg, dst_Src) 
               #print(settings.MEDIA_ROOT)
               #pk=p_desc_obj.pk
               print(p_desc_obj.pk)
               print('huhu')
               img_path_final='class_a/'+fname
               ip_image.img=img_path_final
               ip_image.save()
           #    ip_image.img.save(name,content=ContentFile(zimg),
            #          save=True
          #        )        

 
@receiver(post_save, sender=ClassZipUpload)      
def create_bulk(sender, instance, **kwargs):
   folder=[]
   files=[]
   zpath=instance.zip_file.path
   with ZipFile(instance.zip_file.path, 'r') as zipObj:
      listOfiles = zipObj.namelist()
      for file in listOfiles:
         elem=file
         split=elem.split('/')
         if len(split)>1:
            if split[0] not in folder:
             folder.append(split[0])
             p_desc=ClassPersonDescription.objects.filter(name__exact=split[0]).exists()
             if p_desc is False:
               spo=ClassPersonDescription.objects.create(name=split[0])              
               spo.save()
   print(zpath)
   zip_image(zpath)
  # p = subprocess.Popen([sys.executable, 'image_script.py','--path',zpath], 
                             #       stdout=subprocess.PIPE, 
                             #       stderr=subprocess.STDOUT)
   pass

   
def create_model(sender,instance,created, **kwargs):
   if created:
     inf_path=str(BASE_DIR_PROJECT)
     inf_path=inf_path+'/cnn_web/cnn/'
     p = subprocess.Popen([sys.executable, inf_path+'person_model.py'])
     ClassTrainModel.objects.filter(status='Active').update(status='Old')   

post_save.connect(create_dir, sender=ClassPersonDescription)
pre_delete.connect(remove_dir, sender=ClassPersonDescription)

post_save.connect(create_img, sender=ClassPersonImage)
pre_delete.connect(remove_img, sender=ClassPersonImage)
         
post_save.connect(create_model, sender=ClassTrainModel)

