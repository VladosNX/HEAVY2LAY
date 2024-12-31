bold = '\x1b[1m'
reset = '\x1b[0m'
italic = '\x1b[3m'
version = '1.0.4.1'

msg_help = [
    f'HEAVY2LAY v{version}\n\n',
    f'{bold}ATTENTION:{reset} Use this program only for education and testing goals\n',
    f'Hacking is bad! Be careful!\n\n',
    # mgs_help = msg_help + f'{bold}Usage:{reset} heavy2lay -h <host> -p <port> -s <sockets> -S <sleeptime>\n'
    f'-h <host> - specify target host name\n',
    f'-p <port> - specify target port\n',
    f'-s <sockets> - specify sockets amount\n',
    f'-S <sleeptime> - specify sleep time between loops\n',
    f'{bold}Explanation:{reset}\n',
    f'{italic}Sockets - amount of requests to be sent at the same time\n',
    f'Sleeptime - specifies how long socket will exist{reset}\n\n',
    f'{bold}{italic}Developed by VladosNX, see more my programs on https://github.com/vladosnx'
]

msg_help = ''.join(msg_help)
