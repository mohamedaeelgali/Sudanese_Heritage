import math
from sklearn import neighbors
import os,inspect,sys
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from pathlib import Path
import django

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_MEDIA=Path(__file__).resolve().parent.parent.parent


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

sys.path.insert(0,str(BASE_DIR_MEDIA))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cnn_web.settings'
django.setup()

from cnn_db.models import ClassTrainModel

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []


    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf





if __name__ == "__main__":
    print("Training KNN classifier...")
    imgs_path=BASE_DIR / 'data/Class A'
    classifier = train(imgs_path, model_save_path="trained_knn_model.clf", n_neighbors=2)
    print("Training complete!")
    print(ClassTrainModel.objects.filter(status='Processing').update(status='Active'))