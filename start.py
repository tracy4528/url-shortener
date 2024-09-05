import time
from app import app, db

time.sleep(10)

with app.app_context():
    db.create_all()

app.run(host='0.0.0.0')