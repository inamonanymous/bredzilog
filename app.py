import os
from dotenv import load_dotenv
from flask import Flask 
from routes.routes import rou_bp

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(rou_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)