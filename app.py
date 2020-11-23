from scapy.all import ARP, Ether, srp
import socket
from flask import *
import copy

app=Flask('__main__')
allclients=[]
userinfo={}

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
        allclients.append({'ip': received.psrc, 'mac': received.hwsrc})
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))

#api routes
@app.route('/api/login', methods=['POST'])
def api_login():
    userinfo['name']=request.form['name']
    userinfo['nickname']=request.form['nickname']
    response = make_response(redirect('/session'))
    response.set_cookie('name', request.form['name'])
    response.set_cookie('nicknamename', request.form['nickname'])
    return response

@app.route('/api/getuserinfo', methods=['GET'])
def api_getuserinfo():
    return jsonify(userinfo)

@app.route('/api/getuserlist', methods=['GET'])
def api_getuserlist():
    getallip()
    return jsonify(allclients)

#html routes
@app.route('/')
def flask_index():
    return render_template('index.html')

@app.route('/session')
def flask_session():
    return render_template('session.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
