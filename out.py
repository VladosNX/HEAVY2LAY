import platform
running_platform = platform.system()

def p(text, end='\n'):
    print(text, end=end)

def info(text, left=''):
    if not running_platform == 'Windows':
        print(f'{left}\x1b[44mINFO \x1b[0m {text}')
    else:
        print(f'{left}[INFO ] {text}')
def error(text, left=''):
    if not running_platform == 'Windows':
        print(f'{left}\x1b[41mERROR\x1b[0m {text}')
    else:
        print(f'{left}[ERROR] {text}')
def warn(text, left=''):
    if not running_platform == 'Windows':
        print(f'{left}\x1b[43mWARN \x1b[0m {text}')
    else:
        print(f'{left}[WARN ] {text}')
def done(text, left=''):
    if not running_platform == 'Windows':
        print(f'{left}\x1b[42mDONE \x1b[0m {text}')
    else:
        print(f'{left}[DONE ] {text}')
