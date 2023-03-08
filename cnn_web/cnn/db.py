import os
import django
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_PROJECT=Path(__file__).resolve().parent.parent.parent
print(str(BASE_DIR_PROJECT))
#sys.path.append(BASE_DIR_PROJECT)
sys.path.insert(0,str(BASE_DIR_PROJECT))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnn_web.settings'
django.setup()

from cnn_db.models import ClassPersonDescription

print(ClassPersonDescription.objects.all())
#out: <QuerySet [<Question: WTU?]>