#mongodb+srv://laurafelix2026:<password>@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority

from flask import Flask
from flask import render_template
from flask import request
from pymongo import MongoClient


# -- Initialization section --
app = Flask(__name__)

username = "laurafelix2026"
password = "Papo662607004"
url = f"mongodb+srv://{username}:{password}@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.database

user_input = db.user

all_users = list(user_input.find({}))

all_names=[]

for i in all_users:
    all_names.append(i['name'])

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/auth', methods = ['GET', 'POST'])
def name():
    if request.method == 'POST': 
        name = request.form["name"]
        dictionary_user_name = {'name': name}
        if name not in all_names:
            user_input.insert_one(dictionary_user_name)

        return render_template("bundle_offer.html", props=name, all_names=all_names)
    else:
        return render_template("auth.html")
    

if __name__ == '__main__':
    app.run()
