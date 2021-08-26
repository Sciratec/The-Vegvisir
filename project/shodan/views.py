from flask import Flask, render_template, Blueprint, request, redirect
from shodan import Shodan


shodan_blueprint = Blueprint('shodan', __name__, template_folder='templates')

@shodan_blueprint.route('/shodan', methods=['GET','POST'])
def shodan():
    
    if request.method == "POST":
        req = request.form
        ip = str(req.get('ip'))
        

        api = Shodan("$APIKEY") # Supply own key

        ipInfo = api.host(ip)

        asn = ipInfo['asn']
        country = ipInfo['country_name']
        isp = ipInfo['isp']
        org = ipInfo['org']



        return render_template('shodanresults.html', asn=asn, country=country, isp=isp, org=org, ip=ip)
 

    return render_template('shodan.html')