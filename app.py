from scapy.all import ARP, Ether, srp
import socket
from flask import *
import copy

app=Flask('__main__')
allclients=[]
userinfo={}
global logoutpassword

def getallip():
    myip=str(socket.gethostbyname(socket.gethostname()))
    myip[:myip.rindex('.')]
    target_ip = myip[:myip.rindex('.')]+'.1/24'
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3)[0]
    clients = []
    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    return clients

#api routes
@app.route('/api/login', methods=['POST'])
def api_login():
    global logoutpassword
    userinfo['name']=request.form['name']
    userinfo['nickname']=request.form['nickname']
    logoutpassword=request.form['password']
    response = make_response(redirect('/session'))
    response.set_cookie('name', request.form['name'])
    response.set_cookie('nicknamename', request.form['nickname'])
    return response

@app.route('/api/getuserinfo', methods=['GET'])
def api_getuserinfo():
    return jsonify(userinfo)

@app.route('/api/getuserlist', methods=['GET'])
def api_getuserlist():
    allclients=getallip()
    return jsonify(allclients)

@app.route('/api/relogin', methods=['POST'])
def api_relogin():
    global logoutpassword
    print(logoutpassword)
    print(request.form['password'])
    if logoutpassword!=request.form['password']:
        return 'loginfailure'
    response = make_response(redirect('/session'))
    response.set_cookie('name', userinfo['name'])
    response.set_cookie('nicknamename', userinfo['nickname'])
    return response

#html routes
@app.route('/')
def flask_index():
    print(not bool(userinfo))
    if bool(userinfo):
        return render_template('relogin.html')
    return render_template('index.html')

@app.route('/session')
def flask_session():
    if not bool(userinfo):
        return redirect('/')
    return render_template('session.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
