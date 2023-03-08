from django.contrib import admin
from django.urls import path
from cnn_web import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include


urlpatterns = [
    path('',views.uploading, name='Home'),
    path('admin/', admin.site.urls),
    path("user/", include("django.contrib.auth.urls")), 
    path("add-person/",views.add_person,name="add-person"),
    path("add-structure/",views.add_structure,name="add-structure"),
    path("add-tool/",views.add_tool,name="add-tool")

]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
