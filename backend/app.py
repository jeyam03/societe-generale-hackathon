from flask import Flask, request
from flask_cors import CORS, cross_origin
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api', methods=['POST'])
@cross_origin()
def hello():
    data = request.json
    label_encoder = joblib.load('label_encoder.pkl')

    model = load_model('ml_model.keras')

    tokenizer = Tokenizer()
    tokenizer.num_words = len(model.input[0].shape)

    new_issue = [data['issue']]
    
    # Tokenize the new issue using the same tokenizer used for training
    new_issue_sequences = tokenizer.texts_to_sequences(new_issue)
    new_issue_padded = pad_sequences(new_issue_sequences, maxlen=model.input[0].shape[0], padding='post')

    # Predict the resolution probabilities for the new issue
    predicted_resolution_probs = model.predict(new_issue_padded)

    # Get the class with the highest probability as the predicted class
    predicted_resolution_label = predicted_resolution_probs.argmax(axis=-1)

    # Inverse transform to get the original resolution text
    predicted_resolution = label_encoder.inverse_transform(predicted_resolution_label)

    return predicted_resolution[0]

if __name__ == "__main__":
  app.run()
