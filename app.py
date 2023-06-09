#mongodb+srv://laurafelix2026:<password>@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from pymongo import MongoClient
import bundle_optimization
import custom_bundle

# -- Initialization section --
app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

username = "laurafelix2026"
password = "Papo662607004"
url = f"mongodb+srv://{username}:{password}@cluster0.0ysuf3p.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.database

user_input = db.user

user_input.delete_many({})

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
        return render_template("bundle_offer.html", props=name, bool_check=bool_check, custom_picked=False)
    else:
        return render_template("auth.html")
    
@app.route("/bundle_offer", methods = ['GET', 'POST'])
def money():
    all_info_user = session['users'][-1]
    props = all_info_user['name']
    bool_check=all_info_user['bool_check']
    custom_picked = False
    
    if request.method == 'POST':
        bundle_choice = request.form['button-choice']
        if bundle_choice == str(5):
            stock_name1 = request.form['stock_name1']
            stock_name2 = request.form['stock_name2']
            stock_name3 = request.form['stock_name3']
            stock_name4 = request.form['stock_name4']
            stock_name5 = request.form['stock_name5']

            perf = custom_bundle.stock_info(stock_name1, stock_name2, stock_name3, stock_name4, stock_name5)
            returne = perf[0]
            riske = perf[1]
            custom_picked=True
            weights_info = custom_bundle.read()
            weights = weights_info[1]
            


            return render_template("bundle_offer.html",props=props, bool_check=bool_check, stock_name1=stock_name1, stock_name2=stock_name2, stock_name3=stock_name3, stock_name4=stock_name4, stock_name5=stock_name5, returne=returne, riske=riske, custom_picked=True, weights=weights)
        
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
        return render_template("bundle_offer.html", props= props, bool_check=bool_check, custom_picked=False)

@app.route("/networth", methods=['GET'])
def show_networth_page():
    print(session['users'])
    all_info_user = session['users'][-1]
    props = all_info_user['name']
    bool_check=all_info_user['bool_check']
    bundle_number = all_info_user['bundle_number']
    if bundle_number != str(4):
        user_dicty = list(user_input.find({'name': props}))[0]
        initial_investing_amount = user_dicty['initial_investing_amount']
        percentage_return = round(bundle_optimization.bundle_opt(int(bundle_number))[0]*100,2)
        expected_return = ((percentage_return)/100+1)*initial_investing_amount
        total = expected_return + user_dicty['expected_net_worth']
        user_input.update_one({'name': props},{"$set": {'expected_net_worth': expected_return + user_dicty['expected_net_worth']}})

    else:
        user_dicty = list(user_input.find({'name': props}))[0]
        initial_investing_amount = user_dicty['initial_investing_amount']

        percentage_return = round(custom_bundle.opt_quick()[0]*100,2)
        expected_return = ((percentage_return)/100+1)*initial_investing_amount
        total = round(expected_return + user_dicty['expected_net_worth'],2)
        user_input.update_one({'name': props},{"$set": {'expected_net_worth': expected_return + user_dicty['expected_net_worth']}})


    
    return render_template("/networth.html", props=props, bool_check=bool_check, bundle_number=bundle_number, percentage_return=percentage_return, expected_return=total)

@app.route("/laura", methods=['GET', 'POST'])
def laura():
    if request.method=="GET":
        return render_template("/laura.html")
    else:
        return render_template("/index")

@app.route("/jason", methods=['GET', 'POST'])
def jason():
    if request.method=="GET":
        return render_template("/jason.html")
    else:
        return render_template("/index")

@app.route("/anahi", methods=['GET', 'POST'])
def anahi():
    if request.method=="GET":
        return render_template("/anahi.html")
    else:
        return render_template("/index")
    
if __name__ == '__main__':
    app.run()
