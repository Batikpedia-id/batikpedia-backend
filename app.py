from flask import Flask, render_template, request, redirect
from tensorflow import keras
import tensorflow as tf
from PIL import Image
from io import BytesIO
# from IPython.display import display, clear_output
import numpy as np
import os
from connection import session
import json
from models import Stores, BatikStores, Batik, Users
from storage import upload_blob, delete_blob
from werkzeug.utils import secure_filename
from sqlalchemy.dialects.postgresql import insert
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from google.oauth2 import id_token
from google.auth.transport import requests
from middleware import check_user



import os
from dotenv import load_dotenv
# read from db from environment variable

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

model = tf.keras.models.load_model('ml_models/model.h5')

average_thresholds = {
    "Batik Insang": 0.84,
    "Batik Cendrawasih": 0.78,
    "Batik Kawung": 0.86,
    "Batik Megamendung": 0.91,
    "Batik Parang": 0.83,
    "Batik Poleng": 0.84,
    "Batik Tambal": 0.89
}

# class_labels = ['Batik Cendrawasih', 'Batik Insang', 'Batik Kawung', 'Batik Megamendung', 'Batik Parang', 'Batik Poleng', 'Batik Tambal']
class_labels = ['cendrawasih', 'insang', 'kawung', 'megamendung', 'parang', 'poleng', 'tambal']
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

@app.route('/admin/batik', methods=['GET'])
def dashboard():
    batik = session.query(Batik).all()
    return render_template('admin/batik/index.html', data=batik)

@app.route('/admin/batik/create', methods=['GET'])
def view_create_batik():
    return render_template('admin/batik/create/index.html')

@app.route('/admin/batik/create', methods=['POST'])
def action_create_batik():
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    image = request.files['image']
    

    filename = secure_filename(image.filename)
    image_name = f"{code}.{filename.split('.')[-1]}"
    # # upload_blob(image.filename, "/batik/" + image_name)

    # # create url for image
    

    if image:
        upload_blob(image, "batik/" + image_name)
        image_url = f"https://storage.googleapis.com/batikpedia/batik/{image_name}"



    batik = Batik(name=name, code=code, description=description, image=image_url, image_name=image_name)
    session.add(batik)
    session.commit()

    return render_template('admin/batik/index.html')

@app.route('/admin/batik/edit/<int:id>', methods=['GET'])
def view_edit_batik(id):
    batik = session.query(Batik).filter_by(id=id).first()
    return render_template('admin/batik/edit/index.html', data=batik)

@app.route('/admin/batik/edit/<int:id>', methods=['POST'])
def action_edit_batik(id):
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    image = request.files['image']
    treshold = request.form['treshold']
    batik = session.query(Batik).filter_by(id=id).first()

    # get extension and change image name with code
    filename = secure_filename(image.filename)
    image_name = f"{code}.{filename.split('.')[-1]}"

    if image:
        if batik.image:
            delete_blob("batik/" + batik.image_name)

        print(image_name)

        upload_blob(image, "batik/" + image_name)
        image_url = f"https://storage.googleapis.com/batikpedia/batik/{image_name}"
        batik.image = image_url

    batik.name = name
    batik.code = code
    batik.description = description
    batik.treshold = treshold

    session.commit()

    return redirect('/admin/batik')

@app.route('/admin/batik/delete/<int:id>', methods=['GET'])
def action_delete_batik(id):
    batik = session.query(Batik).filter_by(id=id).first()
    session.delete(batik)
    session.commit()

    return redirect('/admin/batik')

@app.route('/admin/store', methods=['GET'])
def view_stores():
    store = session.query(Stores).all()
    return render_template('admin/store/index.html', data=store)

@app.route('/admin/store/create', methods=['GET'])
def view_create_stores():
    batik = session.query(Batik).all()
    # print(batik)
    return render_template('admin/store/create/index.html', batik_data=batik)

@app.route('/admin/store/create', methods=['POST'])
def action_create_stores():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    instagram = request.form['instagram']
    tokopedia = request.form['tokopedia']
    tiktok = request.form['tiktok']
    batik = request.form.getlist('batik[]')

    store = Stores(name=name, address=address, phone=phone, instagram=instagram, tokopedia=tokopedia, tiktok=tiktok)
    session.add(store)
    session.commit()

    # print(store.id)

    # return ({"success": True, "data": store.to_dict()}, 200)

    for b in batik:
        batik_store = BatikStores(batik_id=b, store_id=store.id)
        session.add(batik_store)
        session.commit()

    session.commit()
    

    return redirect('/admin/store')

    # return ({"success": True}, 200)

@app.route('/admin/store/edit/<int:id>', methods=['GET'])
def view_edit_stores(id):
    batik = session.query(Batik).all()
    store = session.query(Stores).filter_by(id=id).first()
    return render_template('admin/store/edit/index.html', data=store, batik_data=batik)

@app.route('/admin/store/edit/<int:id>', methods=['POST'])
def action_edit_stores(id):
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    instagram = request.form['instagram']
    tokopedia = request.form['tokopedia']
    tiktok = request.form['tiktok']
    batik = request.form.getlist('batik[]')

    store = session.query(Stores).filter_by(id=id).first()
    store.name = name
    store.address = address
    store.phone = phone
    store.instagram = instagram
    store.tokopedia = tokopedia
    store.tiktok = tiktok

    session.commit()

    # delete all batik store
    session.query(BatikStores).filter_by(store_id=id).delete()
    session.commit()

    for b in batik:
        batik_store = BatikStores(batik_id=b, store_id=store.id)
        session.add(batik_store)
        session.commit()

    return redirect('/admin/store')

@app.route('/admin/store/delete/<int:id>', methods=['GET'])
def action_delete_stores(id):
    session.query(BatikStores).filter_by(store_id=id).delete()
    session.commit()
    store = session.query(Stores).filter_by(id=id).first()
    session.delete(store)
    session.commit()

    return redirect('/admin/store')


@app.route('/login/oauth', methods=['POST'])
def loginOauth():
    request = requests.Request()
    token = request.json['token']
    id_info = id_token.verify_oauth2_token(token, request, os.getenv('GOOGLE_CLIENT_ID'))

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return ({"success": False, "message": "Invalid Token"}, 422)
    
    email = id_info['email']
    
    user = session.query(Users).filter_by(username=email).first()

    if not user:
        # create user
        user = Users(username=email, password="")
        session.add(user)
        session.commit()

    access_token = create_access_token(identity=1)


    return ({"success": True, "access_token": access_token}, 200)


@app.post('/predict')
# @check_user
def predict():
    try:
        image = request.files['image'].read()
        predicted_probabilities = predict_image(image)
        
        # change average threshold to a list
        predicted_labels = ""

        # Get highest probability index
        highest_probability_index = np.argmax(predicted_probabilities)

        batik_code = class_labels[highest_probability_index]


        batik = session.query(Batik).filter_by(code=batik_code).first()
        stores = session.query(Stores).join(BatikStores).filter(BatikStores.batik_id == batik.id).limit(5).all()

        if predicted_probabilities[highest_probability_index].item() < batik.treshold:
            return ({
                "success" : False,
                "message": "Batik tidak ditemukan"
            }, 422)
        return {
            "success" : True,
            # "average_thresholds": average_thresholds
            "data": {
                "batik": batik.to_dict(),
                "stores": [store.to_dict() for store in stores]
            },
            "predicted_probabilities": predicted_probabilities[highest_probability_index].item(),
            "message": "Batik Ditemukan"
        }
    except Exception as e:
        print(e)
        return ({
            "success": False,
            "message": "Terdapat kesalahan pada server"
        }, 500)

@app.get('/batik/<int:id>')
def get_batik(id):
    batik = session.get(Batik, id)
    return {
        "success": True,
        "data": batik.to_dict()
    }, 200

@app.get('/batik')
def get_batiks():
    batiks = session.query(Batik).all()
    return {
        "success": True,
        "data": [batik.to_dict() for batik in batiks]
    }, 200

@app.get('/stores')
def get_stores():
    batik_id = request.args.get('batik_id')

    stores = session.query(Stores).join(BatikStores).filter(BatikStores.batik_id == batik_id).all()

    return {
        "success": True,
        "data": [store.to_dict() for store in stores]
    }, 200

if __name__ == '__main__':
    app.run(debug=True)