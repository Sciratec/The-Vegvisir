from flask import render_template, Blueprint

writeups_blueprint = Blueprint('writeups', __name__, template_folder='templates')

@writeups_blueprint.route('/writeups')
def writeups():

    return render_template('writeups.html')