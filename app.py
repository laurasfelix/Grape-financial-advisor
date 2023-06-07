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
        bool_check = False
        name = request.form["name"]
        dictionary_user_name = {'name': name, 'initial_investing_amount': 0, 'expected_net_worth':0 }
        if name not in all_names:
            user_input.insert_one(dictionary_user_name)
            all_users = list(user_input.find({}))
            all_names.append(name)
            for i in all_users:
                all_names.append(i['name'])
        else:
            bool_check=True
            


        return render_template("bundle_offer.html", props=name, bool_check=bool_check)
    else:
        return render_template("auth.html")
    

if __name__ == '__main__':
    app.run()
