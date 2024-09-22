// Function to fetch the Stoic quote from the FastAPI server
async function fetchStoicQuote() {
    try {
        const response = await fetch('https://api.stoic-quote-reader.info/stoic-quote');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log(data);
        document.getElementById("quote").innerText = data.quote;
        document.getElementById("author").innerText = data.author;

        // Start the countdown timer for the next quote
        console.log(data.last_dt)
        startCountdown(data.last_dt);
    } catch (error) {
        console.error('Error fetching Stoic quote:', error);
    }
}

// function to fetch and play the audio file from the server
async function fetchMaleVoice() {
    try {
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
    } catch (error) {
        console.error('Error fetching male audio:', error);
    }
}

async function fetchFemaleVoice() {
    try {
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
    } catch (error) {
        console.error('Error fetching female audio:', error);
    }
}

// Function to calculate the time difference and display the countdown
function startCountdown(lastUpdatedTime) {
    // Convert the last_dt string from the server into a Date object
    const lastUpdatedDate = new Date(lastUpdatedTime);

    // Calculate the next quote update (24 hours after the last update)
    const nextUpdateDate = new Date(lastUpdatedDate.getTime() + 24 * 60 * 60 * 1000);

    // Function to update the countdown every second
    const updateCountdown = () => {
        const now = new Date();
        const timeRemaining = nextUpdateDate - now;

        if (timeRemaining <= 0) {
            document.getElementById("countdown").innerText = "Fetching new quote soon...";
            clearInterval(countdownInterval); // Stop the countdown when time is up
            return;
        }

        // Calculate hours, minutes, and seconds remaining
        const hours = Math.floor(timeRemaining / (1000 * 60 * 60));
        const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

        // Display the countdown
        document.getElementById("countdown").innerText = `${hours}h ${minutes}m ${seconds}s`;
    };

    // Update the countdown every second
    const countdownInterval = setInterval(updateCountdown, 1000);
    updateCountdown(); // Call once to initialize
}
// Fetch the quote when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchStoicQuote();
});



