from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import get
import asyncio

url = 'https://stoic.tekloon.net/stoic-quote'

stoic_quote = None
# Function to grab the stoic quote from the API
async def grab_stoic_quote(time: any):
    global stoic_quote
    try:
        response = get(url)
        data = response.json()

        quote = data["data"].get("quote", "No quote available")
        author = data["data"].get("author", "Unknown author")
        stoic_quote = {"quote": quote, "author": author}
    except Exception as e:
        print(f"Error fetching quote: {e}")

# startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    #run at startup and every 24 hours
    asyncio.create_task(grab_stoic_quote(24 * 60 * 60))
    yield 
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#route to return the current stored stoic quote
@app.get("/stoic-quote")
async def get_stoic_quote():
    if not stoic_quote:
        return {"message": "Quote not available yet. Please try again later."}
    return stoic_quote

@app.get("/")
async def root():
    return {"message": "Hello World"}