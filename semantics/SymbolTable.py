class SymbolTable:
    def __init__(self):
        super().__init__()
        self.symbol_dict = {}

    def put_symbol(self, name, symbol):
        if name in self.symbol_dict:
            raise Exception("Attempt to overwrite a symbol \"" + name + "\"")
        self.symbol_dict.update({name, symbol})

    def remove_symbol(self, name):
        self.symbol_dict.pop(name)

    def contains_symbol(self, name):
        if name in self.symbol_dict:
            return True
        return False
