import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import os
import numpy as np

class AttendanceSystem:
    def __init__(self, known_faces_dir, attendance_file='attendance.xlsx'):
        """
        Initialize the attendance system with known faces directory
        """
        self.known_faces_dir = known_faces_dir
        self.attendance_file = attendance_file
        self.known_faces = []
        self.known_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """
        Load all known faces from the directory
        Filename format: Name_RollNo.jpg (e.g., JohnDoe_101.jpg)
        """
        if not os.path.exists(self.known_faces_dir):
            raise ValueError(f"Directory not found: {self.known_faces_dir}")
        
        print("Loading known faces...")
        print("Expected filename format: Name_RollNo.jpg (e.g., JohnDoe_101.jpg)")
        valid_extensions = ('.jpg', '.jpeg', '.png')
        
        for filename in os.listdir(self.known_faces_dir):
            if filename.lower().endswith(valid_extensions):
                filepath = os.path.join(self.known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(filepath)
                    encodings = face_recognition.face_encodings(image)
                    
                    if len(encodings) > 0:
                        self.known_faces.append(encodings[0])
                        # Extract name without extension and parse name_rollno format
                        name_part = os.path.splitext(filename)[0]
                        self.known_names.append(name_part)
                        print(f"✓ Loaded: {name_part}")
                    else:
                        print(f"✗ No face detected in: {filename}")
                except Exception as e:
                    print(f"✗ Error loading {filename}: {str(e)}")
        
        print(f"\nTotal faces loaded: {len(self.known_faces)}")
    
    def capture_image(self):
        """
        Capture image from webcam with visual feedback
        """
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            print("Error: Could not open webcam")
            return None
        
        print("\n--- Camera opened ---")
        print("Position your face in the frame")
        print("Press SPACE to capture")
        print("Press ESC to cancel")
        
        captured_frame = None
        
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Add instructions overlay
            display_frame = frame.copy()
            cv2.putText(display_frame, "Press SPACE to capture", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, "Press ESC to cancel", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            
            cv2.imshow('Face Recognition Attendance', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space bar
                captured_frame = frame
                print("✓ Image captured!")
                break
            elif key == 27:  # ESC key
                print("Cancelled by user")
                break
        
        cam.release()
        cv2.destroyAllWindows()
        return captured_frame
    
    def recognize_face(self, captured_image, tolerance=0.6):
        """
        Recognize face in the captured image
        tolerance: Lower is more strict (default 0.6)
        Returns: tuple (name, roll_no) or None
        """
        # Convert BGR to RGB (OpenCV uses BGR, face_recognition uses RGB)
        rgb_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
        
        # Find all faces in the image
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if len(face_encodings) == 0:
            print("✗ No faces detected in the image")
            return None
        
        if len(face_encodings) > 1:
            print(f"⚠ Warning: {len(face_encodings)} faces detected. Using the first one.")
        
        captured_encoding = face_encodings[0]
        
        # Compare with known faces
        face_distances = face_recognition.face_distance(self.known_faces, captured_encoding)
        matches = face_recognition.compare_faces(self.known_faces, captured_encoding, tolerance=tolerance)
        
        if True in matches:
            # Get the best match
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                confidence = 1 - face_distances[best_match_index]
                full_name = self.known_names[best_match_index]
                
                # Parse name and roll number from format: Name_RollNo
                if '_' in full_name:
                    parts = full_name.split('_', 1)
                    name = parts[0]
                    roll_no = parts[1]
                else:
                    # Fallback if no underscore found
                    name = full_name
                    roll_no = "N/A"
                
                print(f"✓ Face recognized: {name} (Roll No: {roll_no}, Confidence: {confidence:.2%})")
                return (name, roll_no)
        
        print("✗ Face not recognized")
        return None
    
    def check_duplicate_attendance(self, roll_no, date_str):
        """
        Check if attendance already marked for today
        """
        try:
            df = pd.read_excel(self.attendance_file)
            # Check if student already marked attendance today
            duplicate = df[(df['Roll No'] == roll_no) & (df['Date'] == date_str)]
            return len(duplicate) > 0
        except FileNotFoundError:
            return False
    
    def mark_attendance(self, student_name, roll_no):
        """
        Mark attendance in Excel file with Name and Roll No
        """
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        
        # Check for duplicate
        if self.check_duplicate_attendance(roll_no, current_date):
            print(f"⚠ Attendance already marked for {student_name} (Roll No: {roll_no}) today!")
            return False
        
        try:
            # Try to read existing file
            df = pd.read_excel(self.attendance_file)
        except FileNotFoundError:
            # Create new DataFrame if file doesn't exist with correct column order
            df = pd.DataFrame(columns=["Roll No", "Name", "Date", "Time"])
        
        # Create new record with correct column order
        new_record = pd.DataFrame({
            "Roll No": [roll_no],
            "Name": [student_name],
            "Date": [current_date],
            "Time": [current_time]
        })
        
        # Concatenate and save
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_excel(self.attendance_file, index=False)
        
        print(f"✓ Attendance marked for {student_name} (Roll No: {roll_no}) at {current_time}")
        return True
    
    def run(self):
        """
        Main execution method
        """
        if len(self.known_faces) == 0:
            print("Error: No known faces loaded. Please add face images to the known_faces directory.")
            return
        
        # Capture image
        image = self.capture_image()
        if image is None:
            print("No image captured")
            return
        
        # Recognize face - returns tuple (name, roll_no) or None
        result = self.recognize_face(image)
        if result is None:
            print("Student not recognized!")
            return
        
        student_name, roll_no = result
        
        # Mark attendance
        self.mark_attendance(student_name, roll_no)


def main():
    """
    Main function to run the attendance system
    """
    # Configuration
    known_faces_dir = r'C:\Users\LENOVO\Downloads\Attendence with face\known_faces'
    attendance_file = 'attendance.xlsx'
    
    try:
        # Initialize and run the system
        system = AttendanceSystem(known_faces_dir, attendance_file)
        system.run()
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("\n--- Session ended ---")


if __name__ == "__main__":
    main()