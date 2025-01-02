import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load the dataset
data = pd.read_csv(r'C:/Users/Hi/PycharmProjects/Hamna_FYP/quality_attributes.csv')

# Preprocessing
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['text'])
X = tokenizer.texts_to_sequences(data['text'])
MAX_SEQUENCE_LENGTH = max([len(seq) for seq in X])  # Define MAX_SEQUENCE_LENGTH based on the longest sequence
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)

# Prepare labels
y = pd.get_dummies(data['label']).values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define EMBEDDING_DIM
EMBEDDING_DIM = 1000  # Example dimensionality, adjust as needed

# Build LSTM model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(LSTM(128))
model.add(Dense(len(data['label'].unique()), activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=32)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Accuracy: {accuracy}')

#export
import pickle

# Save the model to a pickle file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)


# Save the tokenizer to a pickle file
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
