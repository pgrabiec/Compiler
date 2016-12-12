class Memory:
    def __init__(self, name):  # memory name
        self.name = name
        self.variables = {}

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):  # gets from memory current value of variable <name>
        return self.variables[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


class MemoryStack:
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.mem_stack = []
        if memory is not None:
            self.mem_stack.append(memory)

    def get(self, name):  # gets from memory stack current value of variable <name>
        size = len(self.mem_stack)
        memory = self.mem_stack[size - 1]
        return memory.get(name)

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.set(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        size = len(self.mem_stack)
        memory = self.mem_stack[size - 1]
        memory.put(name, value)

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.mem_stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.mem_stack.pop()
