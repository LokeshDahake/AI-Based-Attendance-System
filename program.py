import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime
import openpyxl

# Function to load known face encodings and names
def load_known_faces():
    known_faces = []
    known_names = []
    
    # Add more faces as needed
    face_data = [
        {"name": "Narsimha", "file": "photos/narsimha.jpg"},
        {"name": "Uday", "file": "photos/uday.jpg"},
        {"name": "Lokesh", "file": "photos/lokesh.jpg"}
    ]
    
    for person in face_data:
        image = face_recognition.load_image_file(person["file"])
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(person["name"])
    
    return known_faces, known_names

# Function to write attendance to a CSV file
def write_to_csv(file_name, data):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Function to save attendance in Excel
def save_to_excel(file_name, data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Attendance"
    
    # Write headers
    sheet['A1'] = "Name"
    sheet['B1'] = "Time"
    
    # Write attendance data
    for i, row in enumerate(data, start=2):
        sheet[f"A{i}"] = row[0]
        sheet[f"B{i}"] = row[1]
    
    workbook.save(file_name)

# Cleanup function to release camera and close windows
def cleanup(video_capture):
    video_capture.release()
    cv2.destroyAllWindows()
    print("Camera and windows successfully closed")

# Main function for face recognition and attendance
def face_recognition_attendance():
    video_capture = cv2.VideoCapture(0)
    known_face_encodings, known_face_names = load_known_faces()
    students = known_face_names.copy()
    
    # Initialize variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_frame = True
    
    # Get current date and create attendance CSV file
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    csv_file = f"{current_date}.csv"
    l1 = []
    
    while True:
        ret, frame = video_capture.read()
        
        # Check if frame is read correctly
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    face_names.append(name)
                    
                    # Mark attendance
                    if name in students:
                        students.remove(name)
                        current_time = now.strftime("%H-%M-%S")
                        l1.append([name, current_time])
                        print(f"Attendance marked: {name} at {current_time}")
                        
                        # Write to CSV
                        write_to_csv(csv_file, [[name, current_time]])
        
        # Display results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 0, 255), 2)
            cv2.putText(frame, name + " Present", (left * 4, top * 4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        cv2.imshow("Attendance System", frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting the program...")
            break
    
    # Save attendance to Excel
    save_to_excel(f"{current_date}.xlsx", l1)
    print("Attendance saved to Excel")
    
    # Cleanup
    cleanup(video_capture)

if __name__ == "__main__":
    face_recognition_attendance()
