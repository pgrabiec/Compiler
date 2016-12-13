class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # identifier name
        return name in self.variables

    def get(self, name):  # gets from memory current value of identifier <name>
        return self.variables[name]

    def put(self, name, value):  # puts into memory current value of identifier <name>
        self.variables[name] = value


# Example of memories state in the stack (border of viability is determined by the topmost function memory position)
#
# O compound memory (viable)
# O compound memory (viable)
# O loop     memory (viable)
# O compound memory (viable)
# O function memory (viable)
# O compound memory (unavailable)
# O function memory (unavailable)
# O compound memory (unavailable)
# O compound memory (unavailable)
# O BOTTOM
class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.mem_stack = []
        if memory is not None:
            self.mem_stack.append(memory)

    # gets from all viable memories in the stack, returning the value from the most recently added memory
    def get(self, name):
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.has_key(name):
                return memory.get(name)
            i -= 1
        return None

    # checks if the identifier <name> is declared in any of the scopes of the stack
    def has_key(self, name):
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.has_key(name):
                return True
            if memory.name == "function memory":
                return False
            i -= 1
        return False

    # creates or updates entry for identifier <name> with value <value>
    def put_peek(self, name, value):  # inserts into memory stack identifier <name> with value <value>
        size = len(self.mem_stack)
        memory = self.mem_stack[size - 1]
        memory.put(name, value)

    # updates value of identifier <name> in the current viable scope
    def update(self, name, value):
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.has_key(name):
                memory.put(name, value)
            if memory.name == "function memory":
                return
            i -= 1

    # pushes memory <memory> onto the stack
    def push(self, memory):
        self.mem_stack.append(memory)

    # pops the top memory from the stack
    def pop(self):
        self.mem_stack.pop()

    # returns the number of memories in the stack
    def size(self):
        return len(self.mem_stack)

    # pops a layer of compound memories if any
    def pop_compounds(self):
        self.pop_layer_by_name("compound instruction memory")

    # pops the first function memory (along with its compound instruction memory)
    def pop_function(self):
        self.pop_until_name("function memory")
        self.pop_by_name("function memory")

    def pop_until_name(self, name):
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.name == name:
                return
            else:
                self.mem_stack.pop(i)
            i -= 1

    def pop_layer_by_name(self, name):
        popped = False
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.name == name:
                self.mem_stack.pop(i)
                popped = True
            else:
                return popped
            i -= 1
        return popped

    def pop_by_name(self, name):
        size = len(self.mem_stack)
        memory = self.mem_stack[size - 1]
        if memory.name == name:
            self.mem_stack.pop(size - 1)

    def pop_loop(self):
        self.pop_compounds()
        self.pop_by_name("loop memory")

    def pop_compound(self):
        self.pop_by_name("compound instruction memory")

    def is_inside_loop(self):
        size = len(self.mem_stack)
        i = size - 1
        while i >= 0:
            memory = self.mem_stack[i]
            if memory.name == "loop memory":
                return True
            if memory.name == "function memory":
                return False
            i -= 1
        return False;


class MemoryManager:
    def __init__(self):
        super().__init__()
        self.global_memory = Memory("Global memory")
        self.scope_memory = MemoryStack(None)

    def declare(self, name, value):
        if self.scope_memory.size() > 0:
            self.scope_memory.put_peek(name, value)
        else:
            self.global_memory.put(name, value)

    def update_value(self, name, value):
        if self.scope_memory.has_key(name):
            self.scope_memory.update(name, value)
        else:
            if self.global_memory.has_key(name):
                self.global_memory.put(name, value)

    def get_value(self, name):
        value = self.scope_memory.get(name)
        if value is None:
            return self.global_memory.get(name)
        return value

    def push_function_scope(self):
        self.scope_memory.push(Memory("function memory"))

    def push_compound_instructions_scope(self):
        self.scope_memory.push(Memory("compound instruction memory"))

    def push_loop_scope(self):
        self.scope_memory.push(Memory("loop memory"))

    def pop_function_scope(self):
        self.scope_memory.pop_function()

    def pop_compound_instructions_scope(self):
        self.scope_memory.pop_compound()

    def pop_loop_scopes(self):
        if self.scope_memory.is_inside_loop():
            self.scope_memory.pop_loop()

