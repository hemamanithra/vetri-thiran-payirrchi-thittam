// ============================================================
// APPLICATION STATE
// ============================================================

const state = {

    task: "qa"

};


// ============================================================
// TASK CONFIGURATION
// ============================================================

const configs = {

    qa: {

        label: "Ask your question",

        placeholder:
            "Example: What is photosynthesis?",

        button:
            "Get Answer",

        endpoint:
            "/qa",

        key:
            "question"

    },


    explain: {

        label:
            "Enter a topic to explain",

        placeholder:
            "Example: Explain the Pythagoras theorem.",

        button:
            "Explain Topic",

        endpoint:
            "/explain",

        key:
            "text"

    },


    quiz: {

        label:
            "Paste a topic or passage",

        placeholder:
            "Paste your study material here.",

        button:
            "Generate Quiz",

        endpoint:
            "/quiz",

        key:
            "text"

    },


    summary: {

        label:
            "Paste the passage to summarize",

        placeholder:
            "Paste a long educational passage here.",

        button:
            "Summarize",

        endpoint:
            "/summarize",

        key:
            "text"

    },


    learn: {

        label:
            "Enter a topic for your learning path",

        placeholder:
            "Example: Learn Python from beginner to advanced.",

        button:
            "Build Learning Path",

        endpoint:
            "/learn/recommendations",

        key:
            "text"

    }

};


// ============================================================
// DOM ELEMENTS
// ============================================================

const tasks =
    document.querySelectorAll(
        ".task"
    );


const input =
    document.querySelector(
        "#inputText"
    );


const label =
    document.querySelector(
        "#inputLabel"
    );


const buttonText =
    document.querySelector(
        "#buttonText"
    );


const submitButton =
    document.querySelector(
        "#submitBtn"
    );


const form =
    document.querySelector(
        "#studyForm"
    );


const resultCard =
    document.querySelector(
        "#resultCard"
    );


const result =
    document.querySelector(
        "#result"
    );


const loading =
    document.querySelector(
        "#loading"
    );


const count =
    document.querySelector(
        "#charCount"
    );


const statusPill =
    document.querySelector(
        "#statusPill"
    );


const copyButton =
    document.querySelector(
        "#copyBtn"
    );


// ============================================================
// UPDATE UI
// ============================================================

function updateUI() {

    const config =
        configs[state.task];


    label.textContent =
        config.label;


    input.placeholder =
        config.placeholder;


    buttonText.textContent =
        config.button;


    if (state.task === "qa") {

        input.maxLength =
            10000;

    }

    else {

        input.maxLength =
            30000;

    }


    count.textContent =
        `0 / ${input.maxLength}`;

}


// ============================================================
// TASK BUTTONS
// ============================================================

tasks.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                tasks.forEach(
                    (item) => {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                button.classList.add(
                    "active"
                );


                state.task =
                    button.dataset.task;


                updateUI();

            }
        );

    }
);


// ============================================================
// CHARACTER COUNTER
// ============================================================

input.addEventListener(
    "input",
    () => {

        count.textContent =
            `${input.value.length} / ${input.maxLength}`;

    }
);


// ============================================================
// DISPLAY QUIZ
// ============================================================

function showQuiz(data) {

    result.innerHTML = "";


    const questions =
        data.questions || [];


    questions.forEach(
        (question, index) => {

            const wrapper =
                document.createElement(
                    "div"
                );


            wrapper.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h3"
                );


            title.textContent =
                `${index + 1}. ${question.question}`;


            wrapper.appendChild(
                title
            );


            question.options.forEach(
                (option) => {

                    const button =
                        document.createElement(
                            "button"
                        );


                    button.className =
                        "option";


                    button.type =
                        "button";


                    button.textContent =
                        option;


                    button.addEventListener(
                        "click",
                        () => {

                            const allOptions =
                                wrapper.querySelectorAll(
                                    ".option"
                                );


                            allOptions.forEach(
                                (item) => {

                                    item.disabled =
                                        true;


                                    if (
                                        item.textContent
                                        ===
                                        question.answer
                                    ) {

                                        item.classList.add(
                                            "correct"
                                        );

                                    }

                                }
                            );


                            if (
                                option
                                !==
                                question.answer
                            ) {

                                button.classList.add(
                                    "wrong"
                                );

                            }


                            const explanation =
                                document.createElement(
                                    "p"
                                );


                            explanation.className =
                                "quiz-explanation";


                            explanation.textContent =
                                `Explanation: ${question.explanation}`;


                            wrapper.appendChild(
                                explanation
                            );

                        }
                    );


                    wrapper.appendChild(
                        button
                    );

                }
            );


            result.appendChild(
                wrapper
            );

        }
    );

}


// ============================================================
// FORM SUBMISSION
// ============================================================

form.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        const text =
            input.value.trim();


        if (!text) {

            return;

        }


        const config =
            configs[state.task];


        submitButton.disabled =
            true;


        resultCard.hidden =
            false;


        loading.hidden =
            false;


        result.textContent =
            "";


        try {

            const response =
                await fetch(
                    config.endpoint,
                    {

                        method:
                            "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                {
                                    [config.key]:
                                        text
                                }
                            )

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail
                    ||
                    data.result
                    ||
                    "Request failed."
                );

            }


            // Quiz has structured JSON
            if (
                state.task
                ===
                "quiz"
            ) {

                showQuiz(
                    data.result
                );

            }

            else {

                result.textContent =
                    data.result;

            }


            resultCard.scrollIntoView(
                {
                    behavior:
                        "smooth",

                    block:
                        "start"
                }
            );

        }

        catch (error) {

            result.innerHTML =
                "";


            const errorMessage =
                document.createElement(
                    "p"
                );


            errorMessage.className =
                "error";


            errorMessage.textContent =
                error.message;


            result.appendChild(
                errorMessage
            );

        }

        finally {

            loading.hidden =
                true;


            submitButton.disabled =
                false;

        }

    }
);


// ============================================================
// COPY RESULT
// ============================================================

copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );


            copyButton.textContent =
                "Copied!";


            setTimeout(
                () => {

                    copyButton.textContent =
                        "Copy";

                },
                1200
            );

        }

        catch {

            copyButton.textContent =
                "Copy failed";


            setTimeout(
                () => {

                    copyButton.textContent =
                        "Copy";

                },
                1200
            );

        }

    }
);


// ============================================================
// CHECK BACKEND / GEMINI STATUS
// ============================================================

async function checkHealth() {

    try {

        const response =
            await fetch(
                "/health"
            );


        const data =
            await response.json();


        if (
            data.gemini_configured
        ) {

            statusPill.textContent =
                "● Gemini Ready";


            statusPill.style.color =
                "#86efac";

        }

        else {

            statusPill.textContent =
                "● Add Gemini API Key";


            statusPill.style.color =
                "#fcd34d";

        }

    }

    catch {

        statusPill.textContent =
            "● Server Unavailable";

    }

}


// ============================================================
// INITIALIZE
// ============================================================

updateUI();

checkHealth();