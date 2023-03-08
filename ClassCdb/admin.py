from django.contrib import admin
from .models import ClassStructureImage,ClassStructureDescription,ClassZipUpload,ClassTrainModel
from django.http import HttpResponse
from django.utils.translation import ngettext
from django.contrib import messages

#admin.site.register(ClassStructureImage)
#admin.site.register(ClassStructureDescription)




@admin.register(ClassStructureDescription)
class ClassStructureDescriptionAdmin(admin.ModelAdmin):
   
   readonly_fields = ('time',)
   list_display=('name','username','approved')
   ordering = ('name',)
   search_fields = ('name','username','approved')
   
   @admin.action(description='Approve selected items')
   def approve_structure(self, request, queryset):
      count=0  
      for e in queryset:
         count=count+1
         e.approved='y'
         e.save()  

      
      self.message_user(request, ngettext(
            '%d Structure marked as approved.',
            '%d structure marked as approved.',
            count,
        ) % count, messages.SUCCESS)
   actions = [approve_structure]
   


@admin.register(ClassStructureImage)     
class ClassStructureImageAdmin(admin.ModelAdmin):
    
    readonly_fields = ('time',)
    list_display=('name','username','img','approved')
    ordering = ('username',)
    search_fields = ('name__name','username','approved')
    
    @admin.action(description='Approve selected items')
    def approve_image(self, request, queryset):
      count=0  
      for e in queryset:
         count=count+1
         e.approved='y'
         e.save()  

      
      self.message_user(request, ngettext(
            '%d image marked as approved.',
            '%d images marked as approved.',
            count,
        ) % count, messages.SUCCESS)

    def name(self, obj):
      return obj.ClassStructureDescription.name


    actions = [approve_image]

        

@admin.register(ClassZipUpload)
class ClassZipUploadAdmin(admin.ModelAdmin):
   
   readonly_fields = ('time',)
   fields=('comment','zip_file','username')
   list_display=('comment','username','time')
   ordering = ('-time',)
   search_fields = ('comment','username','approved')




@admin.register(ClassTrainModel)
class ClassTrainModelAdmin(admin.ModelAdmin):
   
   readonly_fields = ('time',)
   list_display=('comment','status','time')
   ordering = ('-time',)
   search_fields = ('comment','username','time','status')   

