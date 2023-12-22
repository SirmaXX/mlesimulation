from flask import Blueprint, render_template,url_for,redirect,request,session,flash
from app.Lib.functions import threeweibullcdf,threeweibullpdf,mean_of_threeweibull,variance_of_threeweibull,inverse_of_threeweibull,datagenerator

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