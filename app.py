import os

from flask import Flask
from models import db, connect_db
from main import scrape_mynintendo, message_discord

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# need below line to keep db connection active
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)


@app.get('/')
def show_home_page():
    return "Hi"


@app.get('/scrape')
def call_scrape_fn():
    results = scrape_mynintendo()

    if len(results) != 0:
        message_discord(results)

    return results


with app.app_context():
    db.create_all()
