from django import forms
from django.forms import ModelForm
from cnn_db.models import ClassPersonDescription,ClassPersonImage
from ClassCdb.models import ClassStructureDescription,ClassStructureImage
from Class_D_db.models import ClassToolDescription,ClassToolImage
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox    



class uploadpic(forms.Form):
   image=forms.ImageField(widget= forms.FileInput(attrs={'class':'px-[10px] py-[5px] bg-[#323948] hover:bg-[#181e2a] rounded-md active:scale-[95%] cursor-pointer text-[15px] text-white cursor-pointer',
                   'id':'btn','value':'Browse File'}), label='')
   captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')  


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(PersonForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'
       self.fields['captcha'].required=True
    class Meta:
        model=ClassPersonDescription
        fields = ('name','description','username')
        
        widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'description': forms.Textarea(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(ImageForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'    
    class Meta:
        model=ClassPersonImage
        fields = ('name','img','username')
        widgets = {
        'name': forms.Select(attrs={'class':'form-control'}),
        'img': forms.FileInput(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class StructureForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(StructureForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'
    

    class Meta:
        model=ClassStructureDescription
        fields = ('name','description','username')
        
        widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'description': forms.Textarea(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
class StructureImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(StructureImageForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'    
    class Meta:
        model=ClassStructureImage
        fields = ('name','img','username')
        widgets = {
        'name': forms.Select(attrs={'class':'form-control'}),
        'img': forms.FileInput(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ToolForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(ToolForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'
    

    class Meta:
        model=ClassToolDescription
        fields = ('name','description','username')
        
        widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'description': forms.Textarea(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ToolImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(ToolImageForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'    
    class Meta:
        model=ClassToolImage
        fields = ('name','img','username')
        widgets = {
        'name': forms.Select(attrs={'class':'form-control'}),
        'img': forms.FileInput(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
