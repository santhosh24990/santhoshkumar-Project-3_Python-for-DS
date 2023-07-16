from flask import Flask, render_template, request, jsonify, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)

import pymysql
pymysql.install_as_MySQLdb()


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:8248176784sS@localhost:3306/login_info"
app.config["SQLALCHEMY_TRACK_MODIICATIONS"]=True

db = SQLAlchemy(app)
model= pickle.load(open("model.pkl","rb"))
ss=StandardScaler()
class Logininfo(db.Model):
     id=db.Column(db.Integer,primary_key=True, autoincrement=True)
     username=db.Column(db.String(50))
     password = db.Column(db.String(50))

@app.route("/")
def home():
      return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        check_user=Logininfo(
            username=request.form.get("username"),
            password=request.form.get("password")
        )
        query=db.session.query(Logininfo).filter(Logininfo.username==check_user.username,Logininfo.password==check_user.password)
        result=query.first()
        if result:
            return redirect("predict")
        else:
            return render_template("login.html",login_text="Incorrect Username or Password")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        new_user= Logininfo(
            username=request.form.get("username"),
            password=request.form.get("password")
        )
        query = db.session.query(Logininfo).filter(Logininfo.username == new_user.username)
        result = query.first()
        if result:
            return render_template("register.html", register_text="Username is already registered")
        else:
         db.session.add(new_user)
         db.session.commit()
         return redirect("login")

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method=="GET":
       return render_template("predict.html")
    elif request.method=="POST":
        predict=0
        print("before=",predict)
        features= [ int(x) for x in request.form.values()]
        final_feautres=[np.array(features)]
        scaled_features=ss.fit_transform(final_feautres)
        predict=model.predict(scaled_features)
        print("after=",predict)
        if predict==1:
            return render_template("predict.html", register_text="Your Eligible for the loan")
        else :
            return render_template("predict.html", register_text="your are not eligible")
db.create_all()


if __name__=="__main__":
    app.run(debug=True)