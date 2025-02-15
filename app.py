from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

# Data
vowels = ['a', 'e', 'i', 'o', 'u']
alphabet_unicode = [267, 289, 295, 380, 97, 98, 122] + [*range(100, 121)]
alphabet = [chr(i) for i in alphabet_unicode]
consonants = [chr(i) for i in alphabet_unicode if chr(i) not in vowels]
prohibited_words = {"sex"}  # Prevent inappropriate words

# Game settings
round_no = 15  # Number of rounds before increasing speed
initial_time = 12000  # Start with 12s per round (adjustable)
min_time = 1000  # Minimum time per round (1s)

# Game state
game_state = {
    "current_level": 1,
    "rounds_left": round_no,
    "time_per_round": initial_time,
}


def get_random_letter():
    """Generate a random letter from the alphabet."""
    return random.choice(alphabet)


def get_random_pair():
    """Generate a random consonant-vowel pair."""
    return random.choice(consonants) + random.choice(vowels)


def get_random_triple():
    """Generate a CVC word, avoiding prohibited words."""
    while True:
        word = random.choice(consonants) + random.choice(vowels) + random.choice(consonants)
        if word.lower() not in prohibited_words:
            return word


@app.route('/')
def home():
    """Render the web page."""
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    """Start the game with a chosen level."""
    level = request.json.get('level', 1)
    game_state["current_level"] = level
    game_state["rounds_left"] = round_no
    game_state["time_per_round"] = initial_time
    return jsonify({"message": "Game started", "level": level})


@app.route('/next_round')
def next_round():
    """Generate the next letter/pair/triple and update timing."""
    level = game_state["current_level"]
    if game_state["rounds_left"] > 0:
        game_state["rounds_left"] -= 1
        if level == 1:
            output = get_random_letter()
        elif level == 2:
            output = get_random_pair()
        else:
            output = get_random_triple()
    else:
        # Speed up if rounds are over
        if game_state["time_per_round"] > min_time:
            game_state["time_per_round"] -= 2000  # Make it 2s faster
        game_state["rounds_left"] = round_no
        output = "Faster!"

    return jsonify({"output": output, "time_per_round": game_state["time_per_round"]})


if __name__ == '__main__':
    app.run(debug=True)
