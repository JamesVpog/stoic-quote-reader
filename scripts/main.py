from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from requests import get
import asyncio

import os 
import json 
import datetime as dt 

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

file_path = 'stoic-quote.json'

def write_to_file(file_path, quote_data):
    with open(file_path, 'w') as file:
        json.dump(quote_data, file)

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

url = 'https://stoic.tekloon.net/stoic-quote'

stoic_quote = None
male_audio = None
female_audio = None 

async def grab_stoic_quote():
    global stoic_quote
    try:
        response = get(url)
        data = response.json()

        quote = data["data"].get("quote", "No quote available")
        author = data["data"].get("author", "Unknown author")
        last_dt = dt.datetime.now().isoformat()
        stoic_quote = {"quote": quote, "author": author, "last_dt": last_dt}
        print("Grabbed new quote: ", stoic_quote)
        write_to_file(file_path, stoic_quote)
        
        # After grabbing a new quote, update the audio
        await grab_male_audio()
        await grab_female_audio()
    except Exception as e:
        print(f"Error fetching quote: {e}")

ELEVENLABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

async def grab_male_audio():
    global male_audio
    if not stoic_quote:
        print("No quote available for male audio")
        return

    response = client.text_to_speech.convert(
        voice_id="onwK4e9ZLuTAKqWW03F9", #british authoritative
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=stoic_quote["quote"],
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )

    save_file_path = "male_voice.mp3"

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    male_audio = save_file_path

async def grab_female_audio():
    global female_audio
    if not stoic_quote:
        print("No quote available for female audio")
        return

    response = client.text_to_speech.convert(
        voice_id="pFZP5JQG7iQjIQuC4Bku", # british authoritative
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=stoic_quote["quote"],
        voice_settings=VoiceSettings(
            stability=0.1,
            similarity_boost=0.3,
            style=0.2,
        ),
    )

    save_file_path = "female_voice.mp3"

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    female_audio = save_file_path

@asynccontextmanager
async def lifespan(app: FastAPI):
    global stoic_quote
    if os.path.exists(file_path):
        print(os.path.exists(file_path))
        data = read_from_file(file_path)
        last_updated = dt.datetime.fromisoformat(data['last_dt'])
        if (dt.datetime.now() - last_updated) > dt.timedelta(hours=6): 
            await grab_stoic_quote()
        else:
            stoic_quote = data
            # Check if audio files need to be regenerated
            if not (os.path.exists("male_voice.mp3") and os.path.exists("female_voice.mp3")):
                await grab_male_audio()
                await grab_female_audio()
    else:
        await grab_stoic_quote()
    
    async def periodically_update_stoic_quote():
        while True:
            # await asyncio.sleep(60)  # 1 minute for testing
            await asyncio.sleep(24 * 60 * 60)  # 24 hours
            await grab_stoic_quote()
    
    asyncio.create_task(periodically_update_stoic_quote())
    yield 
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://stoic-quote-reader.info"
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

# route to play the male voice
@app.get("/play-male-voice")
async def play_male_voice():
    file_path = "male_voice.mp3"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename="male_voice.mp3")
    else:
        return {"message": "Male voice not available yet. Please try again later."}

# route to play the female voice
@app.get("/play-female-voice")
async def play_female_voice():
    file_path = "female_voice.mp3"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename="female_voice.mp3")
    else:
        return {"message": "Female voice not available yet. Please try again later."}

@app.get("/")
async def root():
    return {"message": "Hello World"}
