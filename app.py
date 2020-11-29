from flask import *
from flask_socketio import *
from flask_cors import CORS, cross_origin
import socket
import copy
import requests
import json
import secrets

app=Flask('__main__')
socketio=SocketIO(app)
allclients=[]
userinfo={}
sesskey=''
global logoutpassword



#api routes
@app.route('/api/login', methods=['POST'])
def api_login():
    global logoutpassword
    global userinfo
    global sesskey
    sesskey=secrets.token_urlsafe(12)
    userinfo={}
    userinfo['name']=request.form['name']
    userinfo['nickname']=request.form['nickname']
    userinfo['ip']=request.form['ip']
    logoutpassword=request.form['password']
    response = make_response(redirect('/session'))
    response.set_cookie('name', request.form['name'])
    response.set_cookie('nickname', request.form['nickname'])
    response.set_cookie('session', sesskey, httponly=True)
    return response

@app.route('/api/logout', methods=['GET'])
def api_logout():
    if request.cookies.get('session') != sesskey:
        return jsonify({'error' : 'session cookies didn\'t Match'})
    global userinfo
    del userinfo
    logoutpassword=''
    response=make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('nickname')
    response.delete_cookie('session')
    return response

@app.route('/api/getuserinfo', methods=['GET'])
def api_getuserinfo():
    return jsonify(userinfo)

@app.route('/api/getuserlist', methods=['GET'])
def api_getuserlist():
    print(request.cookies.get('session'))
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
    response.set_cookie('session', sesskey)
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
    print(request.cookies.get('session'))
    print('received my event: ' + str(jsonobj))
    js={}
    try:
        r=requests.get('http://'+jsonobj['data']+'/api/getuserinfo')
        js=json.loads(r.text)
        js['found']=True
        js['ip']=jsonobj['data']
        f=open('static/json/friendlist.json','r')
        jst=json.load(f)
        f.close()
        t=js.copy()
        del t['found']
        jst.append(t)
        f=open('static/json/friendlist.json','w')
        f.write(json.dumps(jst, indent=4))
        f.close()
    except Exception as e:
        js['found']=False
        print(e)
    socketio.emit('Add Friend Response', js)


#html routes
@app.route('/')
def flask_index():
    try:
        if bool(userinfo) and request.cookies.get('session')==sesskey:
            return redirect('/session')
    except:
        pass
    try:
        print(not bool(userinfo))
        if bool(userinfo):
            return render_template('relogin.html')
    except:
        print(True)
        return render_template('index.html')
    return render_template('index.html')

@app.route('/session')
def flask_session():
    try:
        if not bool(userinfo):
            return redirect('/')
    except:
        return redirect('/')
    if request.cookies.get('session') != sesskey:
        return redirect('/')
    return render_template('session.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=80)
