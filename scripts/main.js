// Function to fetch the Stoic quote from the FastAPI server
// TODO: use axios 
async function fetchStoicQuote() {
    try {
        // const response = await fetch('http://127.0.0.1:8000/stoic-quote');
        const response = await fetch('https://api.stoic-quote-reader.info/stoic-quote');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        document.getElementById("quote").innerText =  '"' + data.quote + '"';
        document.getElementById("author").innerText = '- ' + data.author;

        // TODO: fix timer
    } catch (error) {
        console.error('Error fetching Stoic quote:', error);
    }
}

// function to fetch and play the audio file from the server
async function fetchMaleVoice() {
    try {
        // const response = await fetch('http://127.0.0.1:8000/play-male-voice');
        const response = await fetch('https://api.stoic-quote-reader.info/play-male-voice');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // response is mp3 file
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        console.log(audioUrl);
        const audio = new Audio(audioUrl);
        audio.play();

        const button = document.getElementById("malebtn");
        const button2 = document.getElementById("femalebtn");
        button.disabled = true;
        button2.disabled = true;

        audio.addEventListener('loadedmetadata', () => {
            const duration = audio.duration;

            // Disable the button and re-enable it after the audio ends
            audio.play();
            setTimeout(() => {
                button.disabled = false;
                button2.disabled = false;
            }, duration * 1000); // Convert duration to milliseconds
        });
    } catch (error) {
        console.error('Error fetching male audio:', error);
    }
}

async function fetchFemaleVoice() {
    try {
        // const response = await fetch('http://127.0.0.1:8000/play-female-voice');
        const response = await fetch('https://api.stoic-quote-reader.info/play-female-voice');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // response is mp3 file
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        console.log(audioUrl);
        const audio = new Audio(audioUrl);
        audio.play();

        const button = document.getElementById("malebtn");
        const button2 = document.getElementById("femalebtn");
        
        button.disabled = true;
        button2.disabled = true;
        audio.addEventListener('loadedmetadata', () => {
            const duration = audio.duration;

            // Disable the button and re-enable it after the audio ends
            audio.play();
            setTimeout(() => {
                button.disabled = false;
                button2.disabled = false;
            }, duration * 1000); // Convert duration to milliseconds
        });
    } catch (error) {
        console.error('Error fetching female audio:', error);
    }
}

// Fetch the quote when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchStoicQuote();
});

// use event listener to listen for male button click
document.getElementById("malebtn").addEventListener("click", fetchMaleVoice);

// use event listener to listen for female button click
document.getElementById("femalebtn").addEventListener("click", fetchFemaleVoice);