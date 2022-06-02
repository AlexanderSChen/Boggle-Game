class BoggleGame {
    // make a new game at this DOM class 

    constructor(boardId, secs = 60) {
        this.secs = secs; //game timer
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        // ticks every 1000ms
        this.timer = setInterval(this.tick.bind(this), 1000);

        // in the element class add-word on submit handleSubmit with bind on this, which is the word entered by the user
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    // shows word in a list of words 
    showWord(word) {
        // in the element class words append key value pair of text: word as a list to the board
        $(".words", this.board).append($("<li>", {text: word}));
    }

    //show score in html
    showScore() {
        // in the element class score set the text to be the current score
        $(".score", this.board).text(this.score);
    }

    //show status message of input word
    showMessage(msg, cls) {
        // in the element class msg set the text to be msg from arg, remove current class, which will be 'ok', 'not-word', 'not-on-board', and add new class which is status of new msg
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }

    //handle submission of word if unique and valid, score, and show

    async handleSubmit(e) {
        // prevent page from refreshing
        e.preventDefault();
        // get value of word from board using jquery and store it in $word
        const $word = $('.word', this.board);

        // set value of word, user input answer, to word variable
        let word = $word.val();
        //if not a word return 
        if(!word) return;

        // checks for duplicate found words
        if(this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }

        //check server for validity
        // response stores result of /check-word
        const resp = await axios.get("/check-word", {params: {word: word }});
        // if not a word, return appropriate message
        if(resp.data.result === "not-word") {
            // use showMessage function to return msg and error as class
            this.showMessage(`${word} is not a valid English word`, "err");
        // if word is not on the board return msg and err classo in showMessage function
        } else if(resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        // if word is unique, exists, and is on the board 
        } else {
            // use showWord function to append it to list of words in HTML
            this.showWord(word);
            // add length of word to score
            this.score += word.length;
            // update score in html
            this.showScore();
            // add word to set of already found words
            this.words.add(word);
            // show message the word was added using showMessage function with ok as class
            this.showMessage(`Added: ${word}`, "ok")
        }

        // reset value of word and focus so word input is focused after word is submitted
        $word.val("").focus();
    }

    //update timer as 1000ms passes in game
    showTimer() {
        //select class timer on board and set text to value of secs
        $(".timer", this.board).text(this.secs);
    }

    // handle tick of timer
    async tick() {
        // reduce secs by 1 every 1000ms
        this.secs -= 1;
        // update timer in html
        this.showTimer();

        // once timer hits 0
        if(this.secs === 0) {
            //clear this timer's interval which stops the timer
            clearInterval(this.timer);
            // run scoreGame() function
            await this.scoreGame();
        }
    }

    // handles end of the game once the timer hits 0 secs
    async scoreGame() {
        // hide the element class add-word so the user is unable to input anymore answers
        $(".add-word", this.board).hide()
        // post the current score so it can be stored in the session
        const resp = await axios.post("/post-score", {score: this.score});
        // if data in response brokeRecord returns true then showMessage of new record
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
}