from flask import Flask, render_template
import random
from datetime import datetime
import requests
current_year = datetime.today().year



app = Flask(__name__)

@app.route('/')
def home_page():
    rand_num = random.randint(1,10)
    current_year = datetime.now().year
    return render_template("index.html", random_number=rand_num, year=current_year)

@app.route('/<name>')
def age_page(name):
    rand_num = random.randint(1,10)
    current_year = datetime.now().year    
    print({name})
    params ={
            "name":{name}
    }
    print(params)
    response = requests.get("https://api.agify.io",params=params)
    age = response.json()['age']
    
    response = requests.get("https://api.genderize.io/",params=params)
    gender = response.json()['gender']
    print(f"{name} {age} {gender}")
    return render_template("newpage.html", random_number=rand_num, year=current_year, age=age, gender=gender,name=name)

if __name__ == "__main__":
    app.run()