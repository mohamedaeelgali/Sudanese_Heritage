from django import forms
from django.forms import ModelForm
from cnn_db.models import ClassPersonDescription,ClassPersonImage


    



class StructureForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(PersonForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'
    

    class Meta:
        model=ClassStructureDescription
        fields = ('name','description','username')
        
        widgets = {
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'description': forms.Textarea(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
       super(ImageForm, self).__init__(*args, **kwargs)
       self.fields['username'].initial = 'anon'    
    class Meta:
        model=ClassStructureImage
        fields = ('name','img','username')
        widgets = {
        'name': forms.Select(attrs={'class':'form-control'}),
        'img': forms.FileInput(attrs={'class':'form-control'}),
        'username': forms.TextInput(attrs={'class':'form-control', 'value':'anon'}),
        }

