import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import spacy
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

main = pd.read_csv('./dataset.csv')
df = main.iloc[:, [1, 2]]
df.head()

nlp = spacy.load("en_core_web_sm")

# Tokenize the "Issue" and "Resolution" columns
df["Issue_tokens"] = df["Issue"].apply(lambda text: [token.text for token in nlp(text)])
df["Resolution_tokens"] = df["Resolution"].apply(lambda text: [token.text for token in nlp(text)])

# Encode the labels (resolutions)
label_encoder = LabelEncoder()
df["Resolution_LabelEncoded"] = label_encoder.fit_transform(df["Resolution"])

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df["Issue_tokens"], df["Resolution_LabelEncoded"], test_size=0.2, random_state=42)

# Create a tokenizer and fit it on the training data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

# Convert text sequences to numerical sequences
X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_test_sequences = tokenizer.texts_to_sequences(X_test)

# Pad sequences to have the same length
max_sequence_length = max(len(seq) for seq in X_train_sequences)
X_train_padded = pad_sequences(X_train_sequences, maxlen=max_sequence_length, padding='post')
X_test_padded = pad_sequences(X_test_sequences, maxlen=max_sequence_length, padding='post')

# Create the text classification model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=max_sequence_length),
    LSTM(64),
    Dense(len(label_encoder.classes_), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_padded, y_train, epochs=10, validation_data=(X_test_padded, y_test))

# Save the Keras model and label encoder
joblib.dump(label_encoder, 'label_encoder.pkl')
model.save('ml_model.keras')

