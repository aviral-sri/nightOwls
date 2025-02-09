# nightOwl-ML-
A model that helps you work all night!


WakeUpCV is your next-generation solution for real-time eye and face detection. Engineered with Flask and OpenCV, this product leverages classical machine learning techniques—using Haar Cascades and Canny Edge Detection—to monitor user alertness efficiently and reliably. Whether you're enhancing driver safety or improving security, WakeUpCV transforms your webcam feed into a dynamic, intelligent monitoring system.

## File Structure

Here's an overview of the project files:

- **H_Eye.xml**  
  Pre-trained Haar Cascade model used for detecting eyes.

- **H_Face.xml**  
  Pre-trained Haar Cascade model used for detecting faces.

- **README.md**  
  This documentation file that provides an overview and instructions for the project.

- **Web.py**  
  The main Flask application that powers the real-time web interface for video processing.

- **beep.wav**  
  Audio file used as the alert sound when the detection criteria are met.

- **main.py**  
  The primary entry point for the application, orchestrating detection routines and module interactions.

## Installation Requirements

To get started with nightOwl, ensure you have the following installed:

- **Python 3.x** – The backbone of our solution.
- **Flask** – Provides a robust, lightweight web interface.
- **opencv-python** – Powers the computer vision operations.
- **numpy** – Enables efficient numerical computations.
