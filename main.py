from flask import Flask, render_template, request
from prompt_generator import generate_prompt
from flap_board import display_on_flap_board

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        prompt = generate_prompt(user_input)
        display_on_flap_board(prompt)  # Simulate displaying on flap board
        return render_template("index.html", prompt=prompt)
    return render_template("index.html", prompt=None)

if __name__ == "__main__":
    app.run(debug=True)