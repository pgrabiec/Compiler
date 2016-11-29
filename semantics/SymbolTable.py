class SymbolTable:
    def __init__(self, name):
        super().__init__()
        self.symbol_dict = {}
        self.scope_name = name

    def put_symbol(self, name, symbol):
        self.symbol_dict.update({name, symbol})

    # Raises KeyError if the mapping is not present
    def get_symbol(self, name):
        return self.symbol_dict[name]

    def contains_symbol(self, name):
        if name in self.symbol_dict:
            return True
        return False
