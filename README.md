# nightOwl-ML-
A model that helps you work all night!

Night Owl is a desktop alertness monitoring application that uses OpenCV for face and eye detection through your webcam. It offers interactive mode selection (normal and hazard) with customizable audio alerts to ensure you're awake and attentive.
Note: We're continuously enhancing Night Owl for better accessibility and more features!


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

- **main.py**  
  The primary entry point for the application, orchestrating detection routines and module interactions.

## Installation Requirements

To get started with nightOwl, ensure you have the following installed:

- **Python 3.x** – The backbone of our solution.
- **Flask** – Provides a robust, lightweight web interface.
- **opencv-python** – Powers the computer vision operations.
- **numpy** – Enables efficient numerical computations.
