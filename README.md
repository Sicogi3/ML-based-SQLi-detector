# Instruction
* To install dependencies ```pip install -r requirements.txt```
* First train the model using ```python train.py```
* (Optional) After training, test the model ```python test.py```
* Run a vulnerable and update the parse request function in ids.py accordinly.
* Currently ids.py looks for query parameters in GET requests of apache access log file and checks if it contains a malicious payload or not (malicious in terms of SQLi)
* This IDS uses Machine Learning to detect SQL injection in apache access logs.
* A 6 layer Neural Networks is used in this IDS (Currently this model is trained on a small dataset - 5000 records)
* Change command in IDS according to environment (Windows/Linux/MacOS)
* After running Docker Container using the command specified in `docker_command.txt`, run ```python ids.py```