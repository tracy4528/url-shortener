import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import logging
import string
import random
from dotenv import load_dotenv
import validators

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

db_user = os.environ.get('POSTGRES_USER', 'postgres')
db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
db_host = os.environ.get('POSTGRES_HOST', 'localhost')
db_port = os.environ.get('POSTGRES_PORT', '5432')
db_name = os.environ.get('POSTGRES_DB', 'url_shortener')

database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

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
def index():
    return app.send_static_file('index.html')

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    original_url = data.get('original_url')

    if not original_url:
        return jsonify({'error': 'Missing original_url'}), 400

    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    existing_url = ShortURL.query.filter_by(original_url=original_url).first()
    if existing_url:
        return jsonify({
            'short_url': request.host_url + existing_url.short_url,
            'expiration_date': existing_url.expiration_date.isoformat(),
            'success': True
        }), 200

    short_url = generate_short_url()
    while ShortURL.query.filter_by(short_url=short_url).first():
        short_url = generate_short_url()

    new_url = ShortURL(original_url=original_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'short_url': request.host_url + short_url,
        'expiration_date': new_url.expiration_date.isoformat(),
        'success': True
    }), 201

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = ShortURL.query.filter_by(short_url=short_url).first()
    if link:
        if link.expiration_date > datetime.utcnow():
            return redirect(link.original_url)
        else:
            return jsonify({'error': 'URL has expired'}), 410
    else:
        abort(404)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)