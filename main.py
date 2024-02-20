from flask import Flask, render_template
import random
from datetime import datetime

current_year = datetime.today().year

app = Flask(__name__)

@app.route('/')
def home_page():
    rand_num = random.randint(1,10)
    # current_year = datetime.today().year()
    return render_template("index.html", random_number=rand_num, year=current_year)

if __name__ == "__main__":
    app.run()