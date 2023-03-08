from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import pathlib
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
import os
from pathlib import Path
from shutil import copy2,copy,move
from zipfile import ZipFile
from django.db import transaction
from django.dispatch import receiver
import subprocess
import sys

sys.path.append("../cnn_web/cnn")
from uuid import uuid4
from django.core.files.base import ContentFile


BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_PROJECT=Path(__file__).resolve().parent.parent


STATUS_CHOICES = [
    ('y', 'Yes'),
    ('n', 'No'),
]

class ClassToolDescription(models.Model):
   name=models.CharField('Tool name', max_length=120)
   description=models.TextField(blank=True, max_length=500)
   username=models.CharField(max_length=60,default="admin")
   approved=models.CharField('Approved',max_length=1, choices=STATUS_CHOICES, default='y')
   ip=models.CharField(max_length=50,default="None")
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)   
   def __str__(self):
      return self.name
         
class ClassToolImage(models.Model):
   name=models.ForeignKey(ClassToolDescription, on_delete=models.CASCADE)
   username=models.CharField(max_length=60,default="admin")
   img=models.ImageField(upload_to='class_d/')   
   approved=models.CharField('Approved',max_length=1, choices=STATUS_CHOICES, default='y')
   time=models.DateTimeField(auto_now_add=True,null=True, blank=True)
   ip=models.CharField(max_length=50,default="None")
   def __str__(self):
      return self.name.name

class ClassZipUpload(models.Model):
   comment=models.CharField('comment', max_length=120)
   zip_file=models.FileField(upload_to='zip/')
   username=models.CharField(max_length=60,default="admin")
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


def create_img(sender, instance, **kwargs):
   print(instance.img.name)
   print(instance.name.name)
   if instance.approved=='y':
     _, ext = os.path.splitext(instance.img.name)
     newname = f'{uuid4()}{ext}'
     newname=instance.name.name+'_'+newname
     data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/class_d/' / newname
     newdbimgname='class_d/'+newname
     img_dir=BASE_DIR_PROJECT / 'media/'
     img_dir=str(img_dir)+'/'+instance.img.name
     img_dir2=str(BASE_DIR_PROJECT / 'media/')+'/'+newdbimgname
     copy2(img_dir,data_dir)
     move(img_dir,img_dir2)
     print(ClassToolImage.objects.filter(img=instance.img.name))
     ClassToolImage.objects.filter(img=instance.img.name).update(img=newdbimgname)



def remove_img(sender, instance, **kwargs):
    img_dir=BASE_DIR_PROJECT / 'media/'
    img_dir=str(img_dir)+'/'+instance.img.name
    imgname_raw=instance.img.name[8:]
    try:
     os.remove(img_dir)
    except:
      print('Error')
    if instance.approved=='y':
    
     data_dir=BASE_DIR_PROJECT / 'cnn_web/cnn/data/class_d/' / imgname_raw
     try:
      os.remove(data_dir) 
     except:
      print('error')

def create_model(sender,instance,created, **kwargs):
   if created:
     inf_path=str(BASE_DIR_PROJECT)
     inf_path=inf_path+'/cnn_web/cnn/'
     p = subprocess.Popen([sys.executable, inf_path+'train_class.py', '--dataset',
'class_d', '--database', 'database_class_d.db','--task','fit'])
     ClassTrainModel.objects.filter(status='Active').update(status='Old')


def zip_image(zpath, instance, **kwargs):
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
               p_desc_obj=ClassToolDescription.objects.get(name=split[0])
               print(p_desc_obj.pk)
               ip_image=ClassToolImage()
               _, ext = os.path.splitext(zimg)
               fname = f'{uuid4()}{ext}'
               print(fname)
               ip_image.name=p_desc_obj
               name_dest='media/class_d/'+fname
               dst_Src=BASE_DIR_PROJECT / name_dest
               copy(zimg, dst_Src) 
               img_path_final='class_d/'+fname
               ip_image.img=img_path_final
               ip_image.save()

   
 
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
             p_desc=ClassToolDescription.objects.filter(name__exact=split[0]).exists()
             if p_desc is False:
               spo=ClassToolDescription.objects.create(name=split[0])              
               spo.save()
   zip_image(zpath,instance)

   pass

   


post_save.connect(create_img, sender=ClassToolImage)
pre_delete.connect(remove_img, sender=ClassToolImage)

post_save.connect(create_model, sender=ClassTrainModel)
