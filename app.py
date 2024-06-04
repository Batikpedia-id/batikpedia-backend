from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from tensorflow import keras
import tensorflow as tf
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, LeakyReLU, Dropout, Activation
# from tensorflow.python.keras.applications import Xception
from PIL import Image
from io import BytesIO
# from IPython.display import display, clear_output
import numpy as np
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# def create_pre_trained_model():
#     pre_trained_model = Xception(
#         input_shape=(224, 224, 3),
#         include_top=False,
#         weights='imagenet',
#         pooling="max"
#     )

#     pre_trained_model.trainable = False

#     return pre_trained_model

# pre_trained_model = create_pre_trained_model()

# def create_final_model(pre_trained_model):
#     inputs = Input(shape=(224, 224, 3))
#     x = pre_trained_model(inputs)
#     x = Dropout(0.3)(x)
#     outputs = Dense(units=7, activation='softmax')(x)
#     model = model(inputs=inputs, outputs=outputs)

#     model.compile(optimizer="adam",
#                   loss="categorical_crossentropy",
#                   metrics=["accuracy"])

#     return model

model = tf.keras.models.load_model('models/model.h5')


# Get class labels
# TRAIN_DIR = 'TRAIN/'
# class_labels = sorted(os.listdir(TRAIN_DIR))

# Define average thresholds for each class
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