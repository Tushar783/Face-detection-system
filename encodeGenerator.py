import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://faceattendancrecognitionsystem-default-rtdb.firebaseio.com/",
                                  'storageBucket': "faceattendancrecognitionsystem.appspot.com"
                              })

# producing 128 dimension of different faces.

folderpath = 'Images'
pathlist = os.listdir(folderpath)
imglist = []
studentID = []
for path in pathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    studentID.append(os.path.splitext(path)[0])

    fileName = f'{folderpath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    #print(path)
    #print(os.path.splitext(path)[0])
#print(studentname)

def findEcoding(imageslist):

    encodeList = []
    for img in imageslist:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("encoding started")
encodinglistknown = findEcoding(imglist)
print(len(imglist))
print(encodinglistknown)
print(len(encodinglistknown))

encodinglistknownwithID = [encodinglistknown, studentID]
print("encoding complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodinglistknownwithID, file)
file.close()
print("file saved")