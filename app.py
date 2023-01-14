import os

from flask import Flask
from models import db, Listings, connect_db
from main import check_items, check_for_changes, scrape_mynintendo

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)


@app.get('/')
def show_home_page():
    return "Hi"


@app.get('/scrape')
def call_scrape_fn():
    results = scrape_mynintendo()
    return results
