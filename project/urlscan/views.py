from flask import Flask, render_template, Blueprint, request, redirect
import requests, json, time

from requests import api

urlscan_blueprint = Blueprint('urlscan', __name__, template_folder='templates')

@urlscan_blueprint.route('/urlscan', methods=['GET','POST'])
def urlscan():
    
    if request.method == "POST":

        scan = request.form["scan"]

        if scan:

            headers = {
            'API-Key':'$APIKEY', #Supply own key 
            'Content-Type':'application/json'
            }

            data = {
            "url": scan,
            "visibility": "public"
            }

            postScan = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
            time.sleep(30)
            jsonLoads = json.loads(postScan.text)
            if jsonLoads['message'] == 'Submission successful':
                phish = "Yes"
                apiResult = requests.get(jsonLoads['api'], headers=headers)
                apiLoads = json.loads(apiResult.text)
                print(apiLoads)
                if "ip" in apiLoads['page']:
                    verdicts = apiLoads['verdicts']
                    url = apiLoads['page']['url']
                    ip = apiLoads['page']['ip']
                    asn = apiLoads['page']['asnname']
                    if "phishing" in verdicts['overall']['tags'] or "phishing" in verdicts['urlscan']['tags'] or "phishing" in verdicts['community']['tags']:
                        return render_template('scanresults.html', url=url, ip=ip, asn=asn,phish=phish)
                    else:
                        clean = "No"
                        return render_template('scanresults.html', clean=clean, url=url)
                else: 
                    noIP = "No IP"
                    return render_template('scanresults.html', noIP=noIP)
            else:
                blacklistCheck = jsonLoads['description']
                return render_template('scanresults.html', blacklistCheck=blacklistCheck)

        
    return render_template('urlscan.html')