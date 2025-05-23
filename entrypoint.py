import os
import json
import numpy as np
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import tflite_runtime.interpreter as tflite
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
MODEL_PATH = 'models/mushroom_classifier.tflite'
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Get class names from the metadata file
with open('models/metadata.txt', 'r') as file:
    class_names = [line.strip() for line in file]

# Load mushroom data from JSON file
def load_mushroom_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading mushroom data from JSON: {e}")
        return {}

# Load the mushroom data
mushroom_data = load_mushroom_data()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Fixed predict_mushroom function using TFLite interpreter
def predict_mushroom(img_path):
    # Load and preprocess image
    img = Image.open(img_path).resize((299, 299))
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalize image (similar to what preprocess_input would do)
    img_array = img_array / 127.5 - 1
    
    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], img_array)
    
    # Run inference
    interpreter.invoke()
    
    # Get the output tensor
    preds = interpreter.get_tensor(output_details[0]['index'])
    
    # Process predictions
    top_indices = np.argsort(preds[0])[-5:][::-1]
    top_predictions = []
    
    for i in top_indices:
        class_name = class_names[i]
        confidence = float(preds[0][i]) * 100
        
        # Search for mushroom data in JSON file
        mushroom_info = next((m for m in mushroom_data if m.get('name', '').lower().replace(" ", "_") == class_name.lower() or 
                              m.get('scientific_name', '').lower().replace(" ", "_") == class_name.lower() or 
                              class_name.split()[0].lower().replace(" ", "_") in m.get('name', '').lower().replace(" ", "_")), None)
        
        if not mushroom_info:
            print("Not Found")
            mushroom_info = {}
        
        info = {
            "scientific_name": mushroom_info.get("scientific_name"),
            "edibility": mushroom_info.get("edibility", "Unknown"),
            "description": mushroom_info.get("description", "No description available"),
            "habitat": mushroom_info.get("habitat", "Unknown"),
            "uses": mushroom_info.get("uses", []),
            "toxicity": mushroom_info.get("toxicity", []),
            "effects": mushroom_info.get("effects", [])
        }
        
        top_predictions.append({
            "class_name": class_name,
            "confidence": confidence,
            "info": info
        })
    
    return top_predictions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                predictions = predict_mushroom(filepath)
                return render_template('index.html', 
                                       filename=filename,
                                       predictions=predictions,
                                       image_path=f'uploads/{filename}')
            except Exception as e:
                return render_template('index.html', error=f'Prediction error: {str(e)}')
        else:
            return render_template('index.html', error='File type not allowed')
    
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)