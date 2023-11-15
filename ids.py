from keras.models import load_model
import pickle
import subprocess
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

log_file_path = "logs/access.log"

print("Starting IDS...")

def parse_apache_log(line): # extract query params from apache log
    payloads = []
    if "GET /" in line:
        query_line = line.split("GET /")[1].split(" HTTP")[0]
        if "?" in query_line:
            query_string = query_line.split("?")[1]
            params = query_string.split("&")
            for param in params:
                if "=" in param:
                    payload = param.split("=")[1]
                    payloads.append(payload)
            
    return payloads

windows_command = f"powershell -Command Get-Content {log_file_path} -Wait"
linux_command = f"tail -f {log_file_path}"

with subprocess.Popen(windows_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
    for line in proc.stdout:
        line = line.decode("utf-8")
        payloads = parse_apache_log(line)
        for payload in payloads:
            if is_sqli(payload):
                print(f"Detected SQLi in {line} with payload {payload}")