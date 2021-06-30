# import libraries

from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import os
from os import path

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def predict():

    response = ""
    predicted_text_english = ""
    predicted_text_urdu = ""
    success = False

    # check if the post request has the file part
    if 'file' not in request.files:
        response = jsonify({'message' : 'No file part in the request'})
        response.status_code = 400
        return response
 
    files = request.files.getlist('file')
     
    for file in files:      
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "download.wav"))
            success = True

    if not success:
        response = jsonify({'message' : 'Cannot find file in the request'})
        response.status_code = 500
        return response

    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "download.wav")
    AUDIO_FILE = os.path.join(app.config['UPLOAD_FOLDER'], "download.wav")
    r = sr.Recognizer()
    
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        predicted_text_urdu = r.recognize_google(audio, language="ur")
        predicted_text_english = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand Audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))

    output = {
        "Predicted Text" : {
            "English" : predicted_text_english,
            "Urdu" : predicted_text_urdu,
        },
        "Gender" : "Male"
    }
    return output

# Route to handle HOME
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predictionresult():

    response = predict()
    google_prediction = response['Predicted Text']['Urdu']
    
    return render_template('index.html', our_model_prediction=google_prediction, google_api_prediction=google_prediction)

@app.route('/predict-api',methods=['POST'])
def prediction_api():
    response = predict()
    return response

if __name__ == "__main__":
    app.run(debug=True)
