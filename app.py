from flask import Flask, abort, make_response, render_template, request, send_file
import os
import modules.wkdverifier as wkdv
import threading as thr
from time import sleep
import logging
import sqlite3
from flask_basicauth import BasicAuth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

postlist = [filename.replace(".html", "") for filename in os.listdir("templates/posts")]

staticlist = [os.path.join(file) for file in os.listdir("static") if os.path.isfile(os.path.join("static", file))]
for root, dirs, files in os.walk("static/.well-known/"):
    for file in files:
        staticlist.append(os.path.join(root, file).replace("static/", ""))

# def bgupdatefilelists(seconds = 120):
#     global postlist
#     while True:
#         postlist = [filename.replace(".html", "") for filename in os.listdir("templates/posts")]
#         logging.info("Updated the postlist")
#         sleep(seconds)

# postlistupdate = thr.Thread(target = bgupdatefilelists)
# postlistupdate.daemon = True
# postlistupdate.start()

def create_app():
    app = Flask(__name__)

    basic_auth = BasicAuth(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/disclaimer")
    def disclaimer():
        return render_template("disclaimer.html")

    @app.route("/donate")
    def donate():
        return render_template("donate.html")

    @app.route("/privacy")
    def privacy():
        return render_template("privacypolicy.html")

    @app.route("/select")
    def select():
        return render_template("select-a-post.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/posts/<apost>")
    def posts(apost):
        if apost in postlist:
            return render_template(f"posts/{apost}.html")
        else:
            ipaddress = request.remote_addr
            logging.warning(f"{ipaddress} tried to access {apost} in /posts but its not in the postlist")
            abort(404)

    # @app.route("/wkd-verify", methods=['GET', 'POST'])
    def wkd():
        results = None
        email = None
        if request.method == 'POST':
            email = request.form['email']
            if "@" not in email:
                abort(403)
            try:
                results = wkdv.fullverify(email)
                logging.info(f"Running wkdv.fullverify for email address {email}")
            except Exception as error:
                results = "error occured"
                ipaddress = request.remote_addr
                logging.error(f"Error occured while using wkdv.fullverify. IP: {ipaddress}, Email: {email} and error: {error}.")
        return render_template("wkd.html", results = results, email = email)

    @app.route("/<path:staticfile>")
    def staticfolder(staticfile):
        if staticfile in staticlist:
            return send_file(f"static/{staticfile}")
        else:
            ipaddress = request.remote_addr
            logging.warning(f"{ipaddress} tried to access a staticfile called {staticfile} but its not in the staticlist")
            abort(404)

    @app.route("/admin")
    @basic_auth.required
    def admin():
        return render_template("admin.html")

    @app.errorhandler(404)
    def notfound404(e):
        return make_response(render_template("404.html"), 404)

    @app.errorhandler(403)
    def forbidden403(e):
        return make_response(render_template("403.html"), 403)

    # app.run(debug=True, host='0.0.0.0')
    return app

# create_app()
