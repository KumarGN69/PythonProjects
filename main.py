from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def home_page():
    rand_num = random.randint(1,10)
    return render_template("index.html", random_number=rand_num)

if __name__ == "__main__":
    app.run()