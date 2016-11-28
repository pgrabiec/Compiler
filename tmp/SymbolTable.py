class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol):
        self.entries[name] = symbol

    def get(self, name, local_only=False):
        try:
            ret = self.entries[name]
            return ret
        except KeyError:
            if not local_only and self.parent is not None:
                return self.parent.get(name)
            else:
                raise

    def newChild(self, name):
        return SymbolTable(self, name)
