from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from tensorflow import keras
import tensorflow as tf
from PIL import Image
from io import BytesIO
# from IPython.display import display, clear_output
import numpy as np
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

model = tf.keras.models.load_model('models/model.h5')

average_thresholds = {
    "Batik Insang": 0.84,
    "Batik Cendrawasih": 0.78,
    "Batik Kawung": 0.86,
    "Batik Megamendung": 0.91,
    "Batik Parang": 0.83,
    "Batik Poleng": 0.84,
    "Batik Tambal": 0.89
}

class_labels = ['Batik Cendrawasih', 'Batik Insang', 'Batik Kawung', 'Batik Megamendung', 'Batik Parang', 'Batik Poleng', 'Batik Tambal']
def predict_image(image):
    img = Image.open(BytesIO(image)).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_probabilities = predictions[0]

    return predicted_probabilities

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.post('/predict')
def predict():
    image = request.files['image'].read()
    predicted_probabilities = predict_image(image)
    
    # change average threshold to a list
    predicted_labels = ""

    # Get highest probability index
    highest_probability_index = np.argmax(predicted_probabilities)

    predicted_labels = class_labels[highest_probability_index]


    print(predicted_labels)
    print(predicted_probabilities[highest_probability_index])
    
    return {
        "predicted_labels": predicted_labels,
        # "average_thresholds": average_thresholds
        "predicted_probabilities": predicted_probabilities[highest_probability_index].item()
    }

if __name__ == '__main__':
    app.run(debug=True)