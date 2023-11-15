from keras.models import load_model
import pickle
import pandas as pd

model_file_path = "sqli_model.keras"
vectorizer_file_path = "vectorizer.pickle"

vectorizer = pickle.load(open(vectorizer_file_path, 'rb'))
model = load_model(model_file_path)

def is_sqli(payload):
    if not model or not vectorizer:
        return False
    
    payload_fit = vectorizer.transform([payload]).toarray()
    payload_df = pd.DataFrame(payload_fit, columns=vectorizer.get_feature_names_out())
    payload_df = payload_df[vectorizer.get_feature_names_out()]

    if model.predict(payload_df)[0][0] >= 0.95:
        is_malicious = True
    else:
        is_malicious = False

    return is_malicious

total = 0
correct = 0

df = pd.read_csv("sqli.csv")
for index, row in df.iterrows():
    total += 1
    try:
        if is_sqli(row['Sentence']) == row['Label']:
            correct += 1
    except:
        pass

print(f"Accuracy: {correct/total}")
        

