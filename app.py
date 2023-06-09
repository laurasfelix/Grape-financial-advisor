#mongodb+srv://laurafelix2026:<password>@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo import MongoClient
import bundle_optimization

# -- Initialization section --
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

username = "laurafelix2026"
password = "Papo662607004"
url = f"mongodb+srv://{username}:{password}@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.database

user_input = db.user

# user_input.delete_many({})

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
    all_users = list(user_input.find({}))
    if len(all_users) == 0:
        session['users'] = []
    if request.method == 'POST': 
        bool_check = False
        name = request.form["name"]
        dictionary_user_name = {'name': name, 'initial_investing_amount': 0, 'expected_net_worth':0 }
        
        
        if name not in all_names:
            user_input.insert_one(dictionary_user_name)
            all_users = list(user_input.find({}))
            all_names.append(name)
            listy = session['users']
            listy.append({'name':name, 'bool_check':False, 'bundle_number': 1})
            session['users'] = listy
           
            

        else:
            listy = session['users']
            listy.append({'name':name, 'bool_check':True, 'bundle_number': 1})
            session['users'] = listy
            bool_check=True

        # return redirect(url_for('.bundle_offer', props=name, bool_check=bool_check))
        return render_template("bundle_offer.html", props=name, bool_check=bool_check)
    else:
        return render_template("auth.html")
    
@app.route("/bundle_offer", methods = ['GET', 'POST'])
def money():
    all_info_user = session['users'][-1]
    props = all_info_user['name']
    bool_check=all_info_user['bool_check']
    
    if request.method == 'POST':
        bundle_choice = request.form['button-choice']
        listy = []
        for i in session['users']:
            if i['name'] == props:
                listy.append({'name': i['name'], 'bool_check':i['bool_check'], 'bundle_number': bundle_choice})
            else:
                listy.append(i)
        session['users'] = listy
        cash = request.form["money-invested"]
        all_users = list(user_input.find({}))
        initial_investing_amount = all_users[all_names.index(props)]['initial_investing_amount']
        user_input.update_one({'name': props},{"$set": {'initial_investing_amount': initial_investing_amount+int(cash)}})
        
        return redirect("/networth")
    else:
        return render_template("bundle_offer.html", props= props, bool_check=bool_check)

@app.route("/networth", methods=['GET'])
def show_networth_page():
    print(session['users'])
    all_info_user = session['users'][-1]
    props = all_info_user['name']
    bool_check=all_info_user['bool_check']
    bundle_number = all_info_user['bundle_number']
    user_dicty = list(user_input.find({'name': props}))[0]
    initial_investing_amount = user_dicty['initial_investing_amount']
    percentage_return = round(bundle_optimization.bundle_opt(int(bundle_number))[0]*100,2)
    expected_return = ((percentage_return)/100+1)*initial_investing_amount
    total = expected_return + user_dicty['expected_net_worth']
    user_input.update_one({'name': props},{"$set": {'expected_net_worth': expected_return + user_dicty['expected_net_worth']}})
    
    return render_template("/networth.html", props=props, bool_check=bool_check, bundle_number=bundle_number, percentage_return=percentage_return, expected_return=total)


if __name__ == '__main__':
    app.run()
