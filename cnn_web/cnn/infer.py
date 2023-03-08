import os,sys
import urllib
from argparse import Namespace
import torch
from PIL import Image
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from cnn_web.cnn.src_files.semantics import ImageNet21kSemanticSoftmax
import timm
from pathlib import Path
from cnn_web.cnn.person_infer import name
from cnn_web.cnn.infer_class import visual_search
import django

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_B=Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR_B))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnn_web.settings'
django.setup()

from cnn_db.models import ClassPersonDescription
from ClassCdb.models import ClassStructureDescription
from Class_D_db.models import ClassToolDescription

args = Namespace()
args.tree_path = BASE_DIR / 'imagenet21k_miil_tree.pth'
semantic_softmax_processor = ImageNet21kSemanticSoftmax(args)
BASE_DIR_MEDIA=Path(__file__).resolve().parent.parent.parent

def inference(imgname):

 try:

  labels = []
  model = timm.create_model('vit_base_patch16_224_miil_in21k', pretrained=True)
  model.eval()
  config = resolve_data_config({}, model=model)
  transform = create_transform(**config)
  imgname_raw=imgname
  imgname='media/uploads/'+imgname
  filename=BASE_DIR_MEDIA / imgname
  img = Image.open(filename).convert('RGB')
  tensor = transform(img).unsqueeze(0)

  with torch.no_grad():
     logits = model(tensor)
     semantic_logit_list = semantic_softmax_processor.split_logits_to_semantic_logits(logits)

     for i in range(len(semantic_logit_list)):
          logits_i = semantic_logit_list[i]

          probabilities = torch.nn.functional.softmax(logits_i[0], dim=0)
          top1_prob, top1_id = torch.topk(probabilities, 1)

          if top1_prob > 0.5:
              top_class_number = semantic_softmax_processor.hierarchy_indices_list[i][top1_id[0]]
              top_class_name = semantic_softmax_processor.tree['class_list'][top_class_number]
              top_class_description = semantic_softmax_processor.tree['class_description'][top_class_name]
              labels.append(top_class_description)

  if 'person' in labels or 'Homo_sapiens_sapiens' in labels or 'Homo_sapiens' in labels or 'homo' in labels:
   p_names=name(imgname_raw)
   p_name_show=""
   p_name_description=""
   coun=0
   for p_name in p_names:
    print(p_name)
    coun=coun+1
    if p_name!='unknown':
     print(ClassPersonDescription.objects.filter(name=p_name))
     p_name_show=p_name_show+" "+str(coun)+".) "+p_name
     p_name_description=p_name_description+str(coun)+".) "+p_name+' '+ClassPersonDescription.objects.get(name=p_name).description+"_"
    else:
      p_name_description=p_name_description+""+str(coun)+".) "+' Unknown'+"_"
   print(p_name_show) 
   p_name_show="Following people have been identified _"+p_name_description
   return p_name_show
  elif 'animal' in labels:
   return_text='Class B: Animals. Details ' 
   count=0
   for each in labels:
     
     if(count>5):
        break
     if each!='animal' or each!='placental' or each!='mammal'  or each!='vertebrate':
         return_text=return_text+'; '+each
     count=count+1    
        
   return return_text
  elif 'Seven_Wonders_of_the_Ancient_World' in labels or 'structure' in labels or 'memorial' in labels or 'Pharaoh' in labels or 'building' in labels or 'stadium' in labels:

   p_name=visual_search(filename,'database_class_c.db','class_c')
   if p_name!='unknown structure':
    return "Following Structure have been identified _"+p_name+" "+ClassStructureDescription.objects.get(name=p_name).description
   else:
     return "Following Structure have been identified _No matching structure"
  # return visual_search(filename,'database_class_c.db','class_c')
   #return 'Class C: Structure'
  elif 'hand_tool' in labels or 'tool' in labels or 'machine' in labels or 'device' in labels:
   print('tool detected')
   p_name=visual_search(filename,'database_class_d.db','class_d')
   print('Tool name:' + p_name)
   if p_name!='unknown tool':
    return "Following Tool have been identified _"+p_name+" "+ClassToolDescription.objects.get(name=p_name).description
   
   else:
    return "Following Tool have been identified _Tool not found"


  # return 'Class D: Tools'
  else:
   return 'Unknown _Please upload an image where the object of interest is discrete and clearly visible'
 
 except Exception as e:
  return e


if __name__ == "__main__": 
    inference() 
