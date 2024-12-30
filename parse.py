T_INT = 0
T_STRING = 1
T_BOOL = 2

class ArgumentNotFound(Exception): pass
class MissingRequiredArgument(Exception): pass

class Parser():
    def __init__(self, argv):
        self.argv = argv
        self.args = {}
    def add_arg(self, name, console_arg, xtype=T_STRING, default=None, required=False):
        self.args[name] = {
            'name': name,
            'xtype': xtype,
            'default': default,
            'console_arg': console_arg,
            'required': required
        }
    def parse(self):
        current_arg = None
        # print(self.argv)
        raw_args = self.argv
        raw_args.pop(0)
        argnames = {}
        for i in self.args:
            # argnames[self.args[i]] = self.args[i]
            # print(i) # debug
            argnames[self.args[i]['console_arg']] = self.args[i]
        result = {}
        for item in raw_args:
            # print(f'parsing {item} with c/a {current_arg}') # debug
            if not current_arg == None:
                # print(f'{current_arg} = {item}') # debug
                # result[args[current_arg]] = item
                # for i in self.args:
                #     if i == current_arg:
                #         result[i] = current_arg
                #         break
                if self.args[current_arg]['xtype'] == T_STRING:
                    result[current_arg] = item
                elif self.args[current_arg]['xtype'] == T_INT:
                    result[current_arg] = int(item)
                current_arg = None
                continue
            elif not item in argnames:
                raise ArgumentNotFound(item)
                continue
            elif argnames[item]['xtype'] == T_BOOL:
                result[argnames[item]['name']] = True
                continue
            else:
                current_arg = argnames[item]['name']
                continue
        for item in self.args:
            ci = self.args[item] # ci - current item
            if ci['required'] and not item in result:
                raise MissingRequiredArgument(item)
            elif ci['xtype'] == T_BOOL and not item in result:
                result[ci['name']] = False
            elif not item in result:
                result[ci['name']] = ci['default']
        return result
