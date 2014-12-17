class SymbolTable(object):
    err = -1
    ok = 0

    def __init__(self, name, parent=None):
        self.parent = parent
        self.dict = {}
        self.name = name

    def put(self, name, symbol):
    #if symbol found, should I swap it?!
        if name in self.dict.keys():
            self.dict[name] = symbol
            return self.err
        else:
            self.dict[name] = symbol
            return self.ok

    def get(self, name):
        if name in self.dict.keys():
            return self.dict[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return self.err


class FunctionsTable(object):

    def __init__(self, name, parent=None):
        self.parent = parent
        self.dict = {}
        self.dicttype = {}
        self.name = name

    err = -1
    ok = 0

    def dicttype(self):
        return self.dicttype

    def putNewFun(self, name, type):
        if name in self.dict.keys():
            self.dict[name] = []
            self.dicttype[name] = type
            return self.err
        else:
            self.dict[name] = []
            self.dicttype[name] = type
            return self.ok

    def put(self, name, symbol):
        if name in self.dict.keys():
            self.dict[name].append(symbol)


    def get(self, name):
        if name in self.dict.keys():
            return self.dict[name], self.dicttype[name]
        if self.parent:
            return self.parent.get(name)
        else:
            return self.err