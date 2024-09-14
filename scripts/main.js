// Function to fetch the Stoic quote from the FastAPI server
async function fetchStoicQuote() {
    try {
        const response = await fetch('http://127.0.0.1:8000/stoic-quote');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
        document.getElementById("quote").innerText = data.quote;
        document.getElementById("author").innerText = data.author;
    } catch (error) {
        console.error('Error fetching Stoic quote:', error);
    }
}

// Fetch the quote when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchStoicQuote();
});


function playMaleVoice() {
        //play the audio file from eleven labs that reads the stoicism quote
        alert("play male voice");
}

function playFemaleVoice() {
        //play the audio file from eleven labs that reads the stoicism quote
        alert("play female voice");
}


