import os
from dotenv import load_dotenv
from flask import Flask 
from routes.user import user_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.debug=True
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4000)
 