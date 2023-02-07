import os

from flask import Flask
from models import db, connect_db
from main import scrape_mynintendo, message_discord, delete_old_records, check_items, get_changes

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

connect_db(app)


@app.get('/')
def show_home_page():
    items = check_items()
    scrape_results = scrape_mynintendo()
    last_change = get_changes()

    display = {
        "current_listings": items,
        "changes": scrape_results,
        "last_change": last_change
    }

    return display


@app.get('/scrape')
def call_scrape_fn():
    results = scrape_mynintendo()

    if results["changes"] != "No changes.":
        message_discord(results["changes"])

    return results


@app.get('/delete')
def delete_records():
    results = delete_old_records()

    return f"Deleted {results} entries."


with app.app_context():
    db.create_all()
