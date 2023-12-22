from flask import Flask, render_template, g, request,session
import pathlib




def unauthorized(e):
    return render_template("assets/403.html"), 403

def page_not_found(e):
    return render_template("assets/404.html"), 404

def internal_server_error(e):
    return render_template("assets/500.html"), 500







def create_app():
    app = Flask(__name__)



    app.register_error_handler(403, unauthorized)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)



    from app.routes.main import main
    app.register_blueprint(main)

   

    return app