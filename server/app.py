import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

from models import db, connect_db
from main import (
    scrape_mynintendo,
    message_discord,
    get_items,
    get_changes,
    load_items,
    get_item_images,
)
from errors import CustomError, CSSTagSelectorError
from routes.check_api import check_api
from routes.main_api import main_api

load_dotenv()


@asynccontextmanager
async def lifespan(app):
    connect_db(app)
    db.create_all()
    yield
    await app.state.db.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace(
#     "postgres://", "postgresql://"
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = False
# # need below line to keep db connection active
# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.state.database_url = os.environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)
app.state.engine_options = {"pool_pre_ping": True}


app.include_router(main_api, prefix="/api")
app.include_router(check_api, prefix="/api")


@app.get("/")
def display_scrape_summary():
    """
    Displays a summary of the scrape, including current listings, images, recent changes, and the last change.
    If changes are found during scraping, notifies via Discord.

    Returns:
        A JSON response containing:
        - current_listings: A list of current items.
        - images: A list of item images.
        - recent_change: The results of the most recent scrape.
        - last_change: Information about the last change detected.
    """

    raw_item_elements = load_items()
    items = get_items(raw_item_elements)
    images = get_item_images(raw_item_elements)
    scrape_results = scrape_mynintendo(items)
    last_change = get_changes()

    if scrape_results["items"] != "No changes.":
        message_discord(scrape_results["items"])

    display = {
        "current_listings": items,
        "images": images,
        "recent_change": scrape_results,
        "last_change": last_change,
    }
    return display


@app.exception_handler(404)
async def not_found_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404, content={"message": "Resource not found."})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, CustomError):
        return JSONResponse(status_code=400, content={"message": str(exc)})
    elif isinstance(exc, CSSTagSelectorError):
        return JSONResponse(status_code=503, content={"message": str(exc)})
    elif isinstance(exc, TimeoutException):
        return JSONResponse(status_code=500, content={"message": str(exc)[9:-1]})
    else:
        return JSONResponse(status_code=500, content={"message": f"{exc}"})


# Middleware for response headers
@app.middleware("http")
async def add_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    return response
