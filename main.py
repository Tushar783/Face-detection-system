import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
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

bucket = storage.bucket()
# setting a webcam for face detection system

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

#importing background image

imgbackground = cv2.imread('Resources/background.png')

#importing modes images to imgmodelist

foldermodepath = 'Resources/modes'
modepathlist = os.listdir(foldermodepath)
imgmodelist = []
for path in modepathlist:
    imgmodelist.append(cv2.imread(os.path.join(foldermodepath, path)))

#print(len(imgmodelist))
#print(imgbackground.shape)

#Load the encoding file
print("loading encode file ......")
file = open('EncodeFile.p', 'rb')
encodinglistknownwithID = pickle.load(file)
file.close()
encodinglistknown, studentID = encodinglistknownwithID
print(studentID)
print("loading complete")
print(len(encodinglistknown))

modeType = 0
counter = 0
ID = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # merging webcam with img background

    imgbackground[120:120 + 480, 80:80 + 640] = img
    imgbackground[7: 7 + 574, 890:890 + 375] = imgmodelist[modeType]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodinglistknown, encodeFace)
        faceDis = face_recognition.face_distance(encodinglistknown, encodeFace)
        #print(matches)
        #print(faceDis)

        matchIndex = np.argmin(faceDis)
        #print("Match Index", matchIndex)

        #if matches[matchIndex]:
        #print("Known Face Detected")
        # print(studentID[matchIndex])
        #else:
        #print("Unknown face detected")

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = 120 + x1, 80 + y1, y2 - y1, x2 - x1
        imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)
        ID = studentID[matchIndex]

        if counter == 0:
            counter = 1
            modeType = 3

    if counter != 0:

        if counter == 1:
            # Get the data
            studentInfo = db.reference(f'Students/{ID}').get()
            print(studentInfo)
            # Get the Image
            blob = bucket.get_blob(f'Images/{ID}.jpg')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            # Update attendance
            ref = db.reference(f'Students/{ID}')
            studentInfo['Attendance'] += 1
            ref.child('Attendance').set(studentInfo['Attendance'])

        if 10<counter<20:
            modeType = 2

        imgbackground[7: 7 + 574, 890:890 + 375] = imgmodelist[modeType]

        if counter <= 10:
            cv2.putText(imgbackground, str(studentInfo['Attendance']), (895, 80),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(imgbackground, str(studentInfo['Name']), (950, 430),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(imgbackground, str(studentInfo['University_Roll_Number']), (950, 500),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

            imgbackground[20:20 + 288, 970:970 + 216] = imgStudent
        counter += 1

        if counter>20:
            counter = 0
            modeType = 0
            studentInfo = []
            imgStudent = []
            imgbackground[7: 7 + 574, 890:890 + 375] = imgmodelist[modeType]


    if img is None:
        print("Image not loaded")
    else:
        #cv2.imshow("Webcamera", img)
        cv2.imshow("Face Attendance", imgbackground)
        cv2.waitKey(1)
