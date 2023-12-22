from flask import Blueprint, render_template,url_for,redirect,request,session,flash


main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@main.route("/index")
def index():
    return render_template("views/main/index.html", title="Homepage")


