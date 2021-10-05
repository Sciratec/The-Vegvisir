from os import error
from flask import Flask, render_template, Blueprint, request, redirect
from shodan import Shodan
import subprocess, re
from project.static.whois import whois

shodan_blueprint = Blueprint('shodan', __name__, template_folder='templates')

@shodan_blueprint.route('/shodan', methods=['GET','POST'])
def shodan():
    
    if request.method == "POST":
        req = request.form
        ip = str(req.get('ip'))
        

        api = Shodan("$APIKEY") # Supply own key

        try:
            ipInfo = api.host(ip)
        except:
            error = "Something went wrong"
            return render_template('shodanresults.html',error=error)

        asn = ipInfo['asn']
        country = ipInfo['country_name']
        isp = ipInfo['isp']
        org = ipInfo['org']
        ports = ipInfo['ports']

        whoisRes = whois(ip)


        return render_template('shodanresults.html',whoisRes=whoisRes, ports=ports, asn=asn, country=country, isp=isp, org=org, ip=ip)
 

    return render_template('shodan.html')