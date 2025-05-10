# NightOwl-ML-

NightOwl-ML- is a desktop application designed to monitor user alertness by detecting facial and eye movements through your webcam. Utilizing OpenCV and pre-trained Haar Cascade models, it offers interactive modes with customizable audio alerts to help users stay attentive during late-night work sessions.

## Features

- **Real-Time Monitoring**: Continuously analyzes webcam feed to detect drowsiness.
- **Mode Selection**: Choose between 'Normal' and 'Hazard' modes based on your alertness needs.
- **Customizable Alerts**: Set personalized audio alerts to prompt you when signs of drowsiness are detected.
- **User-Friendly Interface**: Simple and intuitive design for ease of use.

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/aviral-sri/nightOwls-.git
   cd nightOwl-ML-
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

   This will launch the NightOwl-ML- interface.

## Usage

1. **Launch the Application**: Run `main.py` to start the interface.
2. **Select Mode**: Choose between 'Normal' or 'Hazard' mode based on your preference.
3. **Start Monitoring**: Click on 'Start' to begin real-time alertness monitoring.
4. **Customize Alerts**: Navigate to settings to adjust audio alerts as per your liking.



## File Structure

- `H_Eye.xml`: Pre-trained Haar Cascade model for eye detection.
- `H_Face.xml`: Pre-trained Haar Cascade model for face detection.
- `main.py`: Primary script to run the application.
- `app.py`: Flask application for real-time video processing.
- `templates/`: Directory containing HTML templates for the Flask app.
- `static/`: Directory for static files (CSS, JS, images).
- `README.md`: This documentation file.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/) for the computer vision library.
- [Flask](https://flask.palletsprojects.com/) for the web framework.


