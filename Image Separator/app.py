from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded image
        process_image(file_path)

        return f'File uploaded successfully: {filename}'

    return "Invalid file format"

def process_image(file_path):
    # Load the uploaded image
    image = cv2.imread(file_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply background subtraction (example using MOG2)
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
    fg_mask = bg_subtractor.apply(gray)

    # Perform morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

    # Extract foreground using masking
    foreground = cv2.bitwise_and(image, image, mask=fg_mask)

    # Save the results
    cv2.imwrite('foreground_image.jpg', foreground)
    cv2.imwrite('background_mask.jpg', fg_mask)

if __name__ == '__main__':
    app.run(debug=True)
