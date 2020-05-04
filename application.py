from flask import Flask,render_template,request,url_for,redirect,flash,session,json,make_response
from functools import wraps
import gc
from datetime import date
import datetime
import json
import urllib.request
from pymongo import MongoClient
import sys

var={}

app=Flask(__name__)

client = MongoClient("mongodb+srv://udhay:aakash@cluster0-clxec.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('udhay')
user = db.weather

@app.route('/mongo',methods=['GET','POST'])
def register_student():
    if(len(var)):
        aak="hi"

        user.insert_one({"country_code" : var["country_code"],"coordinate" : var["coordinate"],"temp" : var["temp"],"pressure" : var["pressure"],"humidity" : var["humidity"]})
        col = user.find()
        return render_template('dashboard1.html',col=col)

    else:
        return None


@app.route('/wapi',methods=['POST','GET'])
def weather():

        city = 'mathura'

    # source contain json data from api
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c486181a52d3f129999138533537fff7').read()

        # converting json data to dictionary

        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }

        var["country_code"]= str(list_of_data['sys']['country'])
        var["coordinate"]=str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat'])
        var["temp"]= str(list_of_data['main']['temp']) + 'k'
        var["pressure"]= str(list_of_data['main']['pressure'])
        var["humidity"]= str(list_of_data['main']['humidity'])


        print(data)
        return render_template('index1.html',data=data)

@app.route('/wapi1',methods=['POST','GET'])
def weather1():
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name mathura
        city = 'mathura'

    # source contain json data from api
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=c486181a52d3f129999138533537fff7').read()

    # converting json data to dictionary

    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
    }
    var["country_code"]= str(list_of_data['sys']['country'])
    var["coordinate"]=str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat'])
    var["temp"]= str(list_of_data['main']['temp']) + 'k'
    var["pressure"]= str(list_of_data['main']['pressure'])
    var["humidity"]= str(list_of_data['main']['humidity'])
    print(data)
    return render_template('index1.html',data=data)


app.config['SECRET_KEY']='painthiringbusiness'
cred={}

@app.route("/")
def main():
    
        
    return render_template("index.html")

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('signIn',error="You need to login first"))
    return wrap

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('main'))

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    # read the posted values from the UI
    if request.method=='POST':
        try:
            _username = request.form['inputUsername']
            _phone = request.form['inputPhone']
            _password = request.form['inputPassword']
            _address = request.form['inputAddress']
            _label=request.form['labels']
        except:
            return render_template('signup.html',error="Please fill all the details!!!")

        # validate the received values
        if _username and _phone and _password and _address and (lambda _label:True if _label in ('c','a','o') else False):
            try:
                
                cred[_username]=_password
                return redirect(url_for("main"))

            except Exception as e:
                return render_template('signup.html',error=str(e))

    elif request.method=='GET':
        return render_template('signup.html')


@app.route('/signIn',methods=['GET','POST'])
def signIn():

    if request.method=='GET':
        return render_template('signin.html')
    
    elif request.method=='POST':
        try:
            _username = request.form['inputUsername']
            _label = request.form['labels'] 
            _password = request.form['inputPassword']
        except:
            return render_template('signin.html',error="Please fill all the details!!!")

        # validate the received values
        if _username and _password and (lambda _label:True if _label in ('c','a','o') else False):
            try:
                if (_username in cred.keys()):
                    if (cred[_username]==_password):
                        session['logged_in']=True
                       # session['id'] = 1
                        session['name'] = _username
                        session['label'] = _label
                        #cur.close()
                        return redirect(url_for('dashboard'))
                    else:
                        return render_template('signin.html',error="Please check the details!!!")
                else:
                    return render_template('signin.html',error="Please check the details!!!")
   

            except Exception as e:
                return render_template('signin.html',error=str(e).upper())
        else:
            return render_template('signin.html',error="Please check the details!!!")

@app.route('/dashboard')
@login_required
def dashboard():
    e="1"

    return render_template('dashboard.html',error=e)

cred["Udhay"]="Aakash"




if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=int(sys.argv[1]))
