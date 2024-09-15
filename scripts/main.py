from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import get
import asyncio

import os 
import json 
import datetime as dt 

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

file_path = 'stoic-quote.json'

def write_to_file(file_path,quote_data):
    with open(file_path, 'w') as file:
        data = {
            "data": quote_data,
            "last_updated": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        json.dump(data, file)

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

url = 'https://stoic.tekloon.net/stoic-quote'

stoic_quote = None
# Function to grab the stoic quote from the API
async def grab_stoic_quote():
    global stoic_quote
    try:
        response = get(url)
        data = response.json()

        quote = data["data"].get("quote", "No quote available")
        author = data["data"].get("author", "Unknown author")
        stoic_quote = {"quote": quote, "author": author}
        
        write_to_file(file_path, stoic_quote)
    except Exception as e:
        print(f"Error fetching quote: {e}")

# TODO: using elevenlabs api to play the audio in both male and female voice

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

# startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # first check the file, and then either read the old quote or fetch a new one 
    # based on the 24-hour interval.

    global stoic_quote
    if os.path.exists(file_path):
        data = read_from_file(file_path)
        last_updated = dt.datetime.strptime(data['last_updated'], "%Y-%m-%d %H:%M:%S")
        if (dt.datetime.now() - last_updated) > dt.timedelta(days=1): 
            # if its been more than a day, fetch a new quote and write it to the file
            await grab_stoic_quote()
            write_to_file(file_path, stoic_quote)
        else:
            stoic_quote = data['data']
    else:
        # first time running the server, fetch a new quote
        await grab_stoic_quote()
    
    async def periodically_update_stoic_quote():
        while True:
            await asyncio.sleep(24 * 60 * 60)
            await grab_stoic_quote()
            
    # start the background task
    asyncio.create_task(periodically_update_stoic_quote())
    yield 
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [
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