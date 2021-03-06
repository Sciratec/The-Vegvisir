from flask import Flask, render_template, Blueprint, request, redirect
import requests, json, time

urlscan_blueprint = Blueprint('urlscan', __name__, template_folder='templates')

@urlscan_blueprint.route('/urlscan', methods=['GET','POST'])
def urlscan():
    
    if request.method == "POST":

        scan = request.form["scan"]

        if scan:

            headers = {
            'API-Key':'$APIKEY', # Supply own key
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
                if "message" in apiLoads and apiLoads['status'] != 200:
                    while "message" in apiLoads and apiLoads['status'] != 200:
                        time.sleep(30)
                        apiResult = requests.get(jsonLoads['api'], headers=headers)
                        apiLoads = json.loads(apiResult.text)
                        if "message" not in apiLoads:
                            break
                if "ip" in apiLoads['page']:
                    verdicts = apiLoads['verdicts']
                    url = apiLoads['page']['url']
                    ip = apiLoads['page']['ip']
                    asn = apiLoads['page']['asnname']
                    img = apiLoads['task']['screenshotURL']
                    if "phishing" in verdicts['overall']['tags'] or "phishing" in verdicts['urlscan']['tags'] or "phishing" in verdicts['community']['tags']:
                        hashes = apiLoads['lists']['hashes']
                        hashList = []
                        for ha in hashes[:3]: #Gets 3 IOC hashes and searches for more like phishing content in a 3 day time period
                            hashIOCS = requests.get(f"https://urlscan.io/api/v1/search/?q=(hash:{ha}%20AND%20date:%3Enow-3d)")
                            hashList.append(json.loads(hashIOCS.text))
                        return render_template('scanresults.html', url=url, ip=ip, asn=asn,phish=phish, img=img, hashList=hashList)
                    else:
                        clean = "No"
                        return render_template('scanresults.html', clean=clean, url=url, img=img)
                else: 
                    noIP = f"There is no IP associated with {scan}"
                    return render_template('scanresults.html', noIP=noIP)
            else:
                blacklistCheck = jsonLoads['description']
                return render_template('scanresults.html', blacklistCheck=blacklistCheck)

        
    return render_template('urlscan.html')