import subprocess, re
def whois(value):
    whoIs = subprocess.run(['whois', '-b', value], stdout=subprocess.PIPE).stdout.decode('utf-8')
    whoIsReg = re.findall("inetnum.*|abuse.*", whoIs)

    return whoIsReg
