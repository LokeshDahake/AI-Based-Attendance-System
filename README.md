# Face Recognition Attendance System

This project is a Face Recognition-based Attendance System that uses a webcam to capture images, recognize faces in real-time, and record attendance automatically. It is built using Python, OpenCV, and the `face_recognition` library.

## Features

- Detects and recognizes faces in real-time using a webcam.
- Records the time of attendance for recognized individuals.
- Saves attendance data in both CSV and Excel formats.
- Simple and efficient Python-based implementation.

## Requirements

- Python 3.7+
- Libraries:
  - OpenCV (`cv2`)
  - NumPy
  - `face_recognition`
  - OpenPyXL

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/username/FaceRecognition-Attendance-System.git
    cd FaceRecognition-Attendance-System
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up images**:
    - Add the photos of individuals to the `photos` folder. Ensure each photo is named with the person's name (e.g., `lokesh.jpg`, `narsimha.jpg`, etc.).

4. **Run the program**:
    ```bash
    python face_recognition_attendance.py
    ```

## Usage

- The system will use the webcam to detect faces and compare them with the known faces from the `photos` folder.
- When a face is recognized, the attendance will be recorded along with the current time.
- Attendance is saved to a CSV file named with the current date (e.g., `2024-09-23.csv`) and an Excel file (`2024-09-23.xlsx`).

## Project Structure

