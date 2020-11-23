from scapy.all import ARP, Ether, srp
import socket
from flask import *

app=Flask('__main__')
allclients=[]

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
    allclients=clients
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))

if __name__ == '__main__':
    app.run()
