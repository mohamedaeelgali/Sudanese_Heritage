import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os.path
from pathlib import Path

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp','PNG','JPG','JPEG'}


BASE_DIR = Path(__file__).resolve().parent
BASE_DIR_MEDIA=Path(__file__).resolve().parent.parent.parent

def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.5):
   
    X_img_path='media/uploads/'+X_img_path
    X_img_path=BASE_DIR_MEDIA / X_img_path
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)
    print(len(X_face_locations))
    if len(X_face_locations) == 0:
        return 'not_clear'

    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)


    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def name(file):
    modelpath=BASE_DIR_MEDIA / "trained_knn_model.clf"
    print(modelpath)
    predictions=predict(file, model_path=modelpath)
    names=[]
    for name, (top, right, bottom, left) in predictions:
        print('hey')
        #print(name)
        print(name)
        names.append(name)
        print((top, right, bottom, left))
        #name_one=name
    
    return names

if __name__ == "__main__":
    name()
    predict() 
