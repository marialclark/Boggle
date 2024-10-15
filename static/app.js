class BoggleGame {
    constructor(timerDuration = 60) {
        this.score = 0;
        this.timerDuration = timerDuration;
        this.timer = null;
        this.guessedWords = new Set();
        this.init();
    }

    init() {
        // Start listening for form submissions
        $("form").on("submit", this.handleSubmit.bind(this));
        this.startTimer();
    }

    handleSubmit(evt) {
        evt.preventDefault();  // Prevent page refresh

        if (this.timer) {
            // Get the user's guess and check for duplicates
            const guess = $("input[name='guess']").val().toUpperCase();
            if (this.guessedWords.has(guess)) {
                alert("You've already guessed that word!");
                return;
            }
            this.guessedWords.add(guess);

            // Send the guess to the server
            axios.post('/submit-guess', { guess: guess })
                .then(response => this.handleResponse(response, guess))
                .catch(error => console.error("Error during the request:", error));
        } else {
            alert("Time is up! No more guesses allowed.");
        }
    }

    handleResponse(response, guess) {
        const result = response.data.result;
        console.log("Result from server:", result);

        const guessInput = document.getElementById('guess');

        if (result === 'ok') {
            alert('Great! The word is valid and on the board.');
            this.score += guess.length;
            this.updateScoreDisplay();
        } else if (result === 'not-on-board') {
            alert('The word is valid, but it is not on the board.');
        } else if (result === 'not-word') {
            alert('Sorry, this is not a valid word.');
        }
        guessInput.value = '';
    }

    updateScoreDisplay() {
        $("#score").text("Current Score: " + this.score);
    }

    startTimer() {
        const timerDisplay = $("<div>").attr("id", "timer").appendTo(document.body);
        let seconds = this.timerDuration;

        this.timer = setInterval(() => {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            timerDisplay.text(`Time Remaining: ${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`);

            if (seconds <= 0) {
                clearInterval(this.timer);
                timerDisplay.text("Time's up!");
                this.disableGuessing();
            }
            seconds--;
        }, 1000);
    }

    disableGuessing() {
        $("form").off("submit");
        $("input[name='guess']").prop("disabled", true);
        alert("Time's up! No more guesses allowed.");
        this.endGame();
    }

    endGame() {
        // Send the final score to the server
        axios.post('/update-stats', { score: this.score })
            .then(response => {
                const { games_played, highest_score } = response.data;
                alert(`Game Over! You've played ${games_played} games. Highest Score: ${highest_score}`);
            })
            .catch(error => console.error("Error during the request:", error));
    }
}

// Initialize the game when the page loads
$(document).ready(() => {
    new BoggleGame();
});


// console.log("app.js loaded successfully");
// let score = 0;
// let timer;

// $(function() {
//     // Listen for form submission
//     $("form").on("submit", function(evt) {
//         evt.preventDefault();  // Prevent page refresh

//         if (timer) {
//             // Get the user's guess from the input field
//             const guess = $("input[name='guess']").val().toUpperCase();
//             // console.log("User's guess:", guess); //Debugging

//             // Send a POST request to the server with the guess
//             axios.post('/submit-guess', { guess: guess })
//                 .then(function(response) {
//                     let result = response.data.result;
//                     console.log("Result from server:", result)

//                     // Handle the response and display it to the user
//                     if (result === 'ok') {
//                         alert('Great! The word is valid and on the board.');
//                         score += guess.length;
//                         updateScoreDisplay();
//                     } else if (result === 'not-on-board') {
//                         alert('The word is valid, but it is not on the board.');
//                     } else if (result === 'not-word') {
//                         alert('Sorry, this is not a valid word.');
//                     }
//                 })
//                 .catch(function(error) {
//                     console.error("Error during the request:", error);
//                 });
//         } else {
//             alert("Time is up! No more guesses allowed.");
//         }
//     });
//     startTimer(60);

//     function updateScoreDisplay() {
//         $("#score").text("Current Score: " + score);  // Update the score display
//     }
// });

// function startTimer(duration) {
//     let timerDisplay = document.createElement('div');
//     timerDisplay.id = "timer";
//     document.body.appendChild(timerDisplay);
//     let seconds = duration;

//     timer = setInterval(function() {
//         let minutes = Math.floor(seconds / 60);
//         let remainingSeconds = seconds % 60;

//         // Format time to MM:SS
//         timerDisplay.textContent = `Time Remaining: ${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
        
//         if (seconds <= 0) {
//             clearInterval(timer);
//             timerDisplay.textContent = "Time's up!";
//             disableGuessing();
//         }
//         seconds--;
//     }, 1000);
// }

// function disableGuessing() {
//     $("form").off("submit"); // Disable form submission
//     $("input[name='guess']").prop("disabled", true); // Disable the input field
//     alert("Time's up! No more guesses allowed.");
//     // Optionally, you can send the final score to the server here
//     endGame();
// }

// function endGame() {
//     // Send the final score to the server
//     axios.post('/update-stats', { score: score })
//         .then(function(response) {
//             let gamesPlayed = response.data.games_played;
//             let highestScore = response.data.highest_score;
//             alert(`Game Over! You've played ${gamesPlayed} games. Highest Score: ${highestScore}`);
//         })
//         .catch(function(error) {
//             console.error("Error during the request:", error);
//         });
// }
