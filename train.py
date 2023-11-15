from keras.models import Sequential
from keras import layers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
import nltk
import pickle

nltk.download('stopwords')

dataset_path = "sqli.csv"
model_file_path = "sqli_model.keras"
vectorizer_file_path = "vectorizer.pickle"

print("Loading dataset...")
df = pd.read_csv(dataset_path)

print("Dataset loaded. Preprocessing...")
vectorizer = CountVectorizer(min_df=2, max_df=0.7, stop_words='english')
payloads = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()
transformed_payloads = pd.DataFrame(payloads, columns=vectorizer.get_feature_names_out())

x = transformed_payloads
y = df['Label']

print("Dataset preprocessed. Splitting into train and test...")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
input_dim = x.shape[1]

print("Training model...")
model = Sequential()
model.add(layers.Dense(20, input_dim=input_dim, activation='relu'))
model.add(layers.Dense(10,  activation='tanh'))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, verbose=True, validation_data=(x_test, y_test))

y_pred = model.predict(x_test)
y_pred = [1 if p >= 0.5 else 0 for p in y_pred]

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {0:.4f}".format(accuracy))

model.save(model_file_path)
with open(vectorizer_file_path, 'wb') as f:
    pickle.dump(vectorizer, f)

print(f"Model saved to {model_file_path}")
print(f"Vectorizer saved to {vectorizer_file_path}")