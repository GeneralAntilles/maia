// Update the scores
async function updateScoreAsync(score) {
    return new Promise(async (resolve) => {
        var category = score.classList[0];

        // Add up all the radio button values for questions in this category
        var category_score = 0;
        var values = document.querySelectorAll(
            "." + category + " .form-check > input[type=radio]:checked");

        if (values.length == 0) {
            category_score = "-";
        } else {
            for (var k = 0; k < values.length; k++) {
                var question_score = parseFloat(values[k].value);
                category_score += question_score;
            }
            category_score = (category_score / values.length).toFixed(2);
        }

        // Update the score
        score.innerHTML = category_score;
        if (score.innerHTML == "-") {
            score.style = null;
            resolve();
        } else {
            var score_value_int = parseFloat(score.innerHTML);
            // 0 to 5 scale
            updateScoreColor(score);
            resolve();
        }
        var scores = document.getElementsByClassName("score");
        var total_score = document.getElementById("total-score");
        var total_score_value = 0;
        var total_score_count = 0;
        for (var i = 0; i < scores.length; i++) {
            var score_value = scores[i].innerHTML;
            if (score_value == "-") {
                continue;
            }
            total_score_value += parseFloat(score_value);
            total_score_count += 1;
        }
        if (total_score_count == 0) {
            total_score.innerHTML = "-";
        } else {
            total_score.innerHTML = (total_score_value / total_score_count).toFixed(2);
        }
        updateScoreColor(total_score);
        resolve();
    });
}

async function updateScores() {
    var scores = document.getElementsByClassName("score");
    const scorePromises = [];

    for (var i = 0; i < scores.length; i++) {
        scorePromises.push(updateScoreAsync(scores[i]));
    }

    await Promise.all(scorePromises);
}

// Event listener on radio buttons
var radioButtons = document.querySelectorAll("input[type=radio]");
for (var i = 0; i < radioButtons.length; i++) {
    radioButtons[i].addEventListener("click", function() {
        updateScores();
    });
}

// Event listener on page load
window.addEventListener("load", function() {
    updateScores();
});

function updateScoreColor(ele) {
    var score = parseFloat(ele.innerHTML);
    if (score >= 0 && score <= 1) {
        ele.style.color = "#c14545";
    } else if (score >= 1 && score <= 2) {
        ele.style.color = "#da9938";
    } else if (score >= 2 && score <= 3) {
        ele.style.color = "#e2e241";
    } else if (score >= 3 && score <= 4) {
        ele.style.color = "#44d544";
    } else if (score >= 4 && score <= 5) {
        ele.style.color = "#42c6c6";
    }
}

// Set theme to the user's preferred color scheme
function updateTheme() {
    const colorMode = window.matchMedia("(prefers-color-scheme: dark)").matches ?
      "dark" :
      "light";
    document.querySelector("html").setAttribute("data-bs-theme", colorMode);
  }

  // Set theme on load
  updateTheme()

  // Update theme when the preferred scheme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme)

// Select random radio button for each question
function randomize() {
    var radios = document.querySelectorAll("input[type=radio]");
    for (var i = 0; i < radios.length; i++) {
        var radio = radios[i];
        var random = Math.floor(Math.random() * radio.parentNode.children.length);
        radio.parentNode.children[random].checked = true;
    }
    updateScores();
}

document.getElementById("randomize").addEventListener("click", function () {
    console.log("randomize");
    randomize();
});
