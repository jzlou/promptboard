from flask import Flask, render_template, request
from prompt_generator import DisplayPromptEngine
from flap_board import display_on_flap_board

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        prompt_engine = DisplayPromptEngine()
        system_prompt = prompt_engine.generate_system_prompt(
            content_type="insight",
            chars_per_line=50,
            max_lines=5
        )
        user_prompt = prompt_engine.generate_user_prompt(user_input)
 
        display_on_flap_board(prompt)  # Simulate displaying on flap board
        return render_template("index.html", prompt=prompt)
    return render_template("index.html", prompt=None)

if __name__ == "__main__":
    app.run(debug=True)