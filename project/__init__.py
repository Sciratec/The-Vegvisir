from flask import Flask

app = Flask(__name__)

from project.shodan.views import shodan_blueprint
from project.urlscan.views import urlscan_blueprint

app.register_blueprint(shodan_blueprint)
app.register_blueprint(urlscan_blueprint)