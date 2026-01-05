🎯 Face Recognition Based Attendance System

An automated attendance management system built using Python and Computer Vision that uses face recognition to identify students and mark attendance in real time. The system captures images through a webcam, matches faces with pre-stored images, prevents duplicate attendance, and records data in an Excel file.

📌 Features

📷 Real-time face detection using webcam

🧠 Face recognition using stored face encodings

📝 Automatic attendance marking in Excel

🚫 Prevents duplicate attendance on the same day

⏱ Stores date and time of attendance

🎯 Simple and user-friendly workflow

🛠 Tech Stack

Python

OpenCV

face_recognition

Pandas

NumPy

Excel (.xlsx)

📂 Project Structure
Face-Recognition-Attendance-System/
│
├── known_faces/
│   ├── Gaurav_101.jpg
│   ├── Rahul_102.jpg
│
├── attendance.xlsx
├── main.py
└── README.md


📌 Important:
Each image inside the known_faces folder must follow this format:

Name_RollNo.jpg
Example: Amit_105.jpg

⚙️ How It Works

Loads known face images from the known_faces folder

Encodes faces and stores them in memory

Captures image from webcam

Compares captured face with known faces

If matched, attendance is marked with date & time

Duplicate entries for the same day are avoided

▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
cd Face-Recognition-Attendance-System

2️⃣ Install Required Libraries
pip install opencv-python face-recognition pandas numpy


⚠️ Note:
face_recognition requires dlib, which may need CMake and Visual Studio Build Tools on Windows.

3️⃣ Configure Paths

Open main.py and update:

known_faces_dir = r'path_to_known_faces_folder'
attendance_file = 'attendance.xlsx'

4️⃣ Run the Program
python main.py

📊 Attendance Output Format

The attendance is stored in attendance.xlsx with the following columns:

Roll No	Name	Date	Time
⚠️ Limitations

Works best with proper lighting

Recognizes one face at a time

Requires pre-stored face images

Webcam dependent

🚀 Future Enhancements

Multi-face recognition in one frame

Database integration (MySQL/Firebase)

Web or Mobile application support

Masked face detection

Admin dashboard for attendance management

👨‍💻 Author

Gaurav Rao
B.Tech Student | Web Development | AI & ML Enthusiast
