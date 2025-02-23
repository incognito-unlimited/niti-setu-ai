# backend/app/main.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Niti setu  - Backend is running!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)