from cgitb import reset
from crypt import methods
from flask import Flask, render_template,request,redirect,url_for
import pickle
from datetime import date
import pandas as pd

f = open("random_forest_regression_model.pkl",'rb')
rf_random = pickle.load(f)
print(type(rf_random))

app = Flask(__name__)

@app.route("/")
@app.route("/home",methods=["POST","GET"])
def home():
    result = request.args.get('result',default="")
    return render_template("home.html",title = 'Home',result = result)


@app.route("/predict",methods=["POST","GET"])
def predict():
    if request.method == "POST":

        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = float(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Car_Age = date.today().year - int(request.form["Year"])

        if request.form['Fuel_Type'] == 'Petrol':
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1
        elif request.form['Fuel_Type'] == 'Diesel':
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0

        if request.form['Seller_Type'] == 'Individual':
            Seller_Type_Individual= 1
        else:
            Seller_Type_Individual= 0
        
        if request.form['Transmission'] == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = rf_random.predict([[Present_Price,Kms_Driven,Owner,Car_Age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        result = round(prediction[0],2)
    return redirect(url_for('home',result = result))

if __name__ == '__main__':
    app.run(debug=True)

