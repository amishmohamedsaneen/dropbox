from flask import Flask
from flask_cors import CORS
import os
from routes import routes
from serve import serve

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(routes)
app.register_blueprint(serve)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5050)
