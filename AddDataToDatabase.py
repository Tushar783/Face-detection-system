import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://faceattendancrecognitionsystem-default-rtdb.firebaseio.com/"
                              })

ref = db.reference('Students')

data = {
    "00001":
        {
            "Name": "Ansh Khajuria",
            "University_Roll_Number": 21303023,
            "Branch": "Computer science and Engineering",
            "Starting_Year": 2021,
            "Attendance": 9,
            "Last_attendance_Time": "2024-04-12 09:00:34"



        },
    "00002":
        {
            "Name": "Parul Bhatia",
            "University_Roll_Number": 21303124,
            "Branch": "Computer science and Engineering",
            "Starting_Year": 2021,
            "Attendance": 9,
            "Last_attendance_Time": "2024-04-12 09:00:34"
        },

    "00003":
        {
            "Name": "Shubham Kumar",
            "University_Roll_Number": 21303162,
            "Branch": "Computer science and Engineering",
            "Starting_Year": 2021,
            "Attendance": 9,
            "Last_attendance_Time": "2024-04-12 09:00:34"
        },
    "00004":
        {
            "Name": "Suresh Kumar",
            "University_Roll_Number": 21303174,
            "Branch": "Computer science and Engineering",
            "Starting_Year": 2021,
            "Attendance": 9,
            "Last_attendance_Time": "2024-04-12 09:00:34"
        },
    "00005":
        {
            "Name": "Tushar Jaswal",
            "University_Roll_Number": 21303178,
            "Branch": "Computer science and Engineering",
            "Starting_Year": 2021,
            "Attendance": 9,
            "Last_attendance_Time": "2024-04-12 09:00:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)
