from flask import Flask

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8znxec]/'

from project.shodan.views import shodan_blueprint
from project.urlscan.views import urlscan_blueprint
from project.writeups.views import writeups_blueprint

app.register_blueprint(shodan_blueprint)
app.register_blueprint(urlscan_blueprint)
app.register_blueprint(writeups_blueprint)