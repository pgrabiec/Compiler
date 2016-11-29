from semantics.SymbolTable import SymbolTable


def poll(list_as_stack):
    if len(list_as_stack) < 1:
        raise Exception("Cannot poll an empty stack")
    return list_as_stack[len(list_as_stack) - 1]


class ScopeManager:
    def __init__(self):
        super().__init__()
        self.scopeSymbolTablesStack = []

    def check_scope_present(self, err_msg):
        if len(self.scopeSymbolTablesStack) < 1:
            raise Exception(err_msg)

    def push_scope(self, scope_name):
        self.scopeSymbolTablesStack.append(SymbolTable(scope_name))

    def pop_scope(self):
        self.check_scope_present("Attempt to pop a scope symbol table from empty stack")
        self.scopeSymbolTablesStack.pop()

    def add_scope_symbol(self, name, symbol):
        self.check_scope_present("Cannot add a new scope symbol while there is no scope present")
        scope = poll(self.scopeSymbolTablesStack)
        scope.put_symbol(name, symbol)

    def seek_symbol(self, name):
        for scope in self.scopeSymbolTablesStack:
            if scope.contains_symbol(name):
                return scope.get_symbol(name)
        return None
