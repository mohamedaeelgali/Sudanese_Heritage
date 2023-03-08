from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from cnn_web.cnn.infer import inference
from django.http import HttpResponseRedirect
from .forms import uploadpic,PersonForm,ImageForm,StructureForm,StructureImageForm,ToolForm,ToolImageForm
from cnn_db.models import ClassPersonDescription
from cnn_db.models import ClassPersonImage
from ClassCdb.models import ClassStructureDescription
from ClassCdb.models import ClassStructureImage
from Class_D_db.models import ClassToolDescription
from Class_D_db.models import ClassToolImage
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def uploading(request):
   context ={}
   
   if request.method == 'POST':
     uploadedform=uploadpic(request.POST,request.FILES)
     if uploadedform.is_valid():
      uploaded_files= request.FILES['image']
      locpath=BASE_DIR / 'media/uploads/'
      fs=FileSystemStorage(location=locpath,base_url='/media/uploads/')
      name=fs.save(uploaded_files.name,uploaded_files)
      classname=inference(name)
      print('here')
      print('class name: '+classname)
      classnametit=classname.split('_')
      title=classnametit[0]
      classnametit.pop(0)
      context['img']=fs.url(name)
      context['classname']=classnametit
      print(str(classnametit))
      context['title']=title
      try:
       if 'Unknown' in classname:
         context['unknown']='True'
       if 'Tool not found' in classname: 

         context['unknown_tool']='True'      
       if 'No matching structure' in classname:
         context['unknown_structure']='True' 
      except Exception as e:
        print(e) 
     else:
      print(uploadedform.errors)
      return HttpResponseRedirect('/?captcha_submitted=True')
   if 'captcha_submitted' in request.GET:
    captcha_submitted=True
    context['captcha_submitted']=True
   context['uploadpic']=uploadpic
   return render(request,'class.html',context)


def add_person(request):
  person_submitted= False
  image_submitted= False
  context={}
  if request.method == 'POST':
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.POST.get("type", False)=='person':
     person_form=PersonForm(request.POST)
     if person_form.is_valid():
      pform=ClassPersonDescription(
      name=request.POST.get("name", False),
      description=request.POST.get("description", False),
      username=request.POST.get("username", False),
      approved='n',
      ip=ip
        )
      pform.save()      
      return HttpResponseRedirect('/add-person?person_submitted=True')

     else:
      return HttpResponseRedirect('/add-person?captcha_submitted=True')
    if request.POST.get("type", False)=='image':
      
      image_form=ImageForm(request.POST,request.FILES) 
      print(image_form.errors)
      person_val=request.POST.get("name", False)
      person_instance=ClassPersonDescription.objects.get(pk=person_val)
      if image_form.is_valid():
        
        iform=ClassPersonImage(
        name=person_instance,
        img=request.FILES['img'],
        username=request.POST.get("username", False),
        approved='n',
        ip=ip
        )
        iform.save()
        return HttpResponseRedirect('/add-person?image_submitted=True')
      else:
       return HttpResponseRedirect('/add-person?captcha_submitted=True')
  if 'person_submitted' in request.GET:
    person_submitted=True
    context['person_submitted']='A new person has been addedd'
  if 'image_submitted' in request.GET:
    image_submitted=True
    context['image_submitted']='A new image has been addedd'    
  if 'captcha_submitted' in request.GET:
    captcha_submitted=True
    context['captcha_submitted']='Captcha missing'
  context['person_form']=PersonForm
  context['image_form']=ImageForm
  return render(request,'add_person.html',context)



def add_structure(request):
  structure_submitted= False
  image_submitted= False
  context={}
  if request.method == 'POST':
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.POST.get("type", False)=='person':
     structure_form=StructureForm(request.POST)
     if structure_form.is_valid():
      pform=ClassStructureDescription(
      name=request.POST.get("name", False),
      description=request.POST.get("description", False),
      username=request.POST.get("username", False),
      approved='n',
      ip=ip
        )
      pform.save()      
      return HttpResponseRedirect('/add-structure?structure_submitted=True')
     else:
       return HttpResponseRedirect('/add-tool?captcha_submitted=True')
    if request.POST.get("type", False)=='image':
      
      structure_image_form=StructureImageForm(request.POST,request.FILES) 
      print(structure_image_form.errors)
      person_val=request.POST.get("name", False)
      structure_instance=ClassStructureDescription.objects.get(pk=person_val)
      if structure_image_form.is_valid():
        
        iform=ClassStructureImage(
        name=structure_instance,
        img=request.FILES['img'],
        username=request.POST.get("username", False),
        approved='n',
        ip=ip
        )
        iform.save()
        return HttpResponseRedirect('/add-structure?image_submitted=True')

      else:
       return HttpResponseRedirect('/add-tool?captcha_submitted=True')

  
  if 'structure_submitted' in request.GET:
    person_submitted=True
    context['structure_submitted']='A new structure has been addedd'
  if 'image_submitted' in request.GET:
    image_submitted=True
    context['image_submitted']='A new image has been addedd'    
  if 'captcha_submitted' in request.GET:
    captcha_submitted=True
    context['captcha_submitted']='Captcha missing'


  context['structure_form']=StructureForm
  context['structure_image_form']=StructureImageForm
  return render(request,'add_structure.html',context)  


def add_tool(request):
  tool_submitted= False
  image_submitted= False
  context={}
  if request.method == 'POST':
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.POST.get("type", False)=='person':
     tool_form=ToolForm(request.POST)
     if tool_form.is_valid():
      pform=ClassToolDescription(
      name=request.POST.get("name", False),
      description=request.POST.get("description", False),
      username=request.POST.get("username", False),
      approved='n',
      ip=ip
        )
      pform.save()      
      return HttpResponseRedirect('/add-tool?tool_submitted=True')
     else:
       return HttpResponseRedirect('/add-tool?captcha_submitted=True')


    if request.POST.get("type", False)=='image':
      
      tool_image_form=ToolImageForm(request.POST,request.FILES) 
      print(tool_image_form.errors)
      tool_val=request.POST.get("name", False)
      tool_instance=ClassToolDescription.objects.get(pk=tool_val)
      if tool_image_form.is_valid():
        
        iform=ClassToolImage(
        name=tool_instance,
        img=request.FILES['img'],
        username=request.POST.get("username", False),
        approved='n',
        ip=ip
        )
        iform.save()
        return HttpResponseRedirect('/add-tool?image_submitted=True')
      else:
       return HttpResponseRedirect('/add-tool?captcha_submitted=True')

  
  if 'tool_submitted' in request.GET:
    tool_submitted=True
    context['tool_submitted']='A new tool has been addedd'
  if 'image_submitted' in request.GET:
    image_submitted=True
    context['image_submitted']='A new image has been addedd'    
  if 'captcha_submitted' in request.GET:
    captcha_submitted=True
    context['captcha_submitted']='Captcha missing'


  context['tool_form']=ToolForm
  context['tool_image_form']=ToolImageForm
  return render(request,'add_tool.html',context)    
