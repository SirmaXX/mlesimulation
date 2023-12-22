from flask import Blueprint, render_template,url_for,redirect,request,session,flash
from app.Lib.functions import threeweibullcdf,threeweibullpdf,mean_of_threeweibull,variance_of_threeweibull,inverse_of_threeweibull,datagenerator
import numpy as np
main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@main.route("/index")
def index():
    return render_template("views/main/index.html", title="Homepage")


@main.route("/distrosimulation", methods=["GET", "POST"])
def weibulldistrosimulation():
    if request.method == "GET":
        return render_template("views/main/distrosimulation.html")
    elif request.method == "POST":
        alpha = float(request.form["alpha"])
        beta = float(request.form["beta"])
        eta = float(request.form["eta"])
    
        return render_template("views/main/distrosimulation.html", alpha=alpha, beta=beta, eta=eta, title="Distrosimulation") 
    else:
        return "Beklenmedik web istegi"
    




@main.route("/nsimulation", methods=["GET", "POST"])
def nsimulation():
    if request.method == "GET":
        liste=[]
        return render_template("views/main/nbased.html" ,liste=liste, title="Distrosimulation")
    elif request.method == "POST":
        n= int(request.form["n"])
        alpha = float(request.form["alpha"])
        beta = float(request.form["beta"])
        eta = float(request.form["eta"])
        datas = datagenerator(n, alpha, beta, eta)
        gercekortalama=mean_of_threeweibull(alpha, beta, eta)
        gercekvaryans=variance_of_threeweibull(alpha, beta, eta)
        uretilenortama=np.mean(datas)
        uretilenvaryans=np.var(datas)
        liste=[n,alpha,beta,eta,gercekortalama,gercekvaryans,uretilenortama,uretilenvaryans]
        return render_template("views/main/nbased.html", liste=liste, title="Distrosimulation") 
    else:
        return "Beklenmedik web istegi"