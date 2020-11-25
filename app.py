from flask import *
from flask_socketio import *
from flask_cors import CORS, cross_origin
import socket
import copy
import requests
import json

app=Flask('__main__')
socketio=SocketIO(app)
allclients=[]
userinfo={}
global logoutpassword



#api routes
@app.route('/api/login', methods=['POST'])
def api_login():
    global logoutpassword
    userinfo['name']=request.form['name']
    userinfo['nickname']=request.form['nickname']
    userinfo['ip']=request.form['ip']
    logoutpassword=request.form['password']
    response = make_response(redirect('/session'))
    response.set_cookie('name', request.form['name'])
    response.set_cookie('nickname', request.form['nickname'])
    return response

@app.route('/api/getuserinfo', methods=['GET'])
def api_getuserinfo():
    return jsonify(userinfo)

@app.route('/api/getuserlist', methods=['GET'])
def api_getuserlist():
    f=open('static/json/friendlist.json','r')
    js=json.load(f)
    return jsonify(js)

@app.route('/api/relogin', methods=['POST'])
def api_relogin():
    global logoutpassword
    print(logoutpassword)
    print(request.form['password'])
    if logoutpassword!=request.form['password']:
        return 'loginfailure'
    response = make_response(redirect('/session'))
    response.set_cookie('name', userinfo['name'])
    response.set_cookie('nickname', userinfo['nickname'])
    socketio.emit('Different Login', {'date':'Login From different Device'})
    return response

@app.route('/api/sendmsg', methods=['POST'])
@cross_origin()
def api_sendmsg():
    js=request.get_json()
    print(js)
    socketio.emit('Message Received', js)
    return 'test'

@socketio.on('Add Friend')
def api_addfriend(jsonobj, methods=['GET', 'POST']):
    print('received my event: ' + str(jsonobj))
    js={}
    try:
        r=requests.get('http://'+jsonobj['data']+'/api/getuserinfo')
        js=json.loads(r.text)
        js['found']=True
        js['ip']=jsonobj['data']
    except Exception as e:
        js['found']=False
        print(e)
    socketio.emit('Add Friend Response', js)


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
    socketio.run(app, debug=True, host='0.0.0.0', port=80)
