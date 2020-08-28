from app import app
from db import db

db.init_app(app

# Create the database using sqlalchemy
@app.before_first_request
def create_tables():
    db.create_all())