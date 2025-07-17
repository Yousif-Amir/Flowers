from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
model = load_model("./Models/flower_model.h5")
classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    img_path = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Preprocess image
            img = image.load_img(filepath, target_size=(150, 150))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            pred = model.predict(img_array)
            prediction = classes[np.argmax(pred)]
            img_path = filepath

    return render_template("index.html", prediction=prediction, img_path=img_path)

if __name__ == "__main__":
    app.run(debug=True)
