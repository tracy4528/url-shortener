import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import logging
import string
import random
import pymysql
from dotenv import load_dotenv
load_dotenv()

pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'root')
db_host = os.environ.get('DB_HOST', 'localhost')
db_name = os.environ.get('DB_NAME', 'url_shortener')

database_url = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"Using database URL: {database_url}")

try:
    db = SQLAlchemy(app)
    logger.info("Successfully initialized SQLAlchemy")
except Exception as e:
    logger.error(f"Error initializing SQLAlchemy: {str(e)}")
    raise

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(8), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, original_url, short_url, expiration_days=30):
        self.original_url = original_url
        self.short_url = short_url
        self.expiration_date = datetime.utcnow() + timedelta(days=expiration_days)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)