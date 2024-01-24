from flask import Blueprint, render_template,url_for,redirect,request,session,flash
from app.Lib.functions import mean_of_threeweibull,variance_of_threeweibull,datagenerator,mle_es_func,least_reg_func,wls,wls_bergman,wls_ft
from app.Lib.functions import cma_es_func,mean_of_inversechi,variance_of_inversechi
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
    



@main.route("/incchidistro", methods=["GET", "POST"])
def incchidistro():
    if request.method == "GET":
        return render_template("views/main/inchidistrosimulation.html")
    elif request.method == "POST":
        v = float(request.form["v"])
        mean= mean_of_inversechi(v)
        variance= variance_of_inversechi(v)
        return render_template("views/main/inchidistrosimulation.html", v=v, mean=mean,variance=variance,  title="Distrosimulation") 
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
    




@main.route("/estimators", methods=["GET", "POST"])
def estimators():
    if request.method == "GET":
        liste=mleparameters= cmaes=leastsq=wls_one=wls_bergmann= wls_ftt=[]   
        return render_template("views/main/estimator.html" ,liste=liste,mleparameters=  mleparameters, cmaes= cmaes,leastsq=leastsq,wls_one=wls_one,wls_bergmann=wls_bergmann,wls_ftt=wls_ftt ,title="Distrosimulation")
    elif request.method == "POST":
        n= int(request.form["n"])
        alpha = float(request.form["alpha"])
        beta = float(request.form["beta"])
        eta = float(request.form["eta"])
        datas = datagenerator(n, alpha, beta, eta)
        mleparameters=mle_es_func(datas, alpha, beta, eta)
        cmaes=cma_es_func(datas, alpha, beta, eta)
        leastsq=least_reg_func(datas, alpha, beta, eta)
        wls_one=wls(datas, alpha, beta, eta)
        wls_bergmann=wls_bergman(datas, alpha, beta, eta)
        wls_ftt=wls_ft(datas, alpha, beta, eta)
        liste=[n,alpha,beta,eta]
        
        return render_template("views/main/estimator.html", liste=liste, mleparameters=mleparameters, cmaes=cmaes, leastsq=leastsq, wls_one=wls_one, wls_ftt=wls_ftt, wls_bergmann=wls_bergmann, title="Distrosimulation")
    else:
        return "Beklenmedik web istegi"
    





@main.route("/presentation", methods=["GET", "POST"])
def presentation():
    return render_template("views/main/presentation.html", title="Homepage")