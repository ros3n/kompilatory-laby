

class Memory:

    data = {}

    def __init__(self, name): # memory name
        self.name = name

    def has_key(self, name):  # variable name
        return name in self.data

    def get(self, name):         # get from memory current value of variable <name>
        return self.data[name]


    def put(self, name, value):  # puts into memory current value of variable <name>
        self.data[name] = value


class MemoryStack:

    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if memory:
            self.stack.append(memory)
        self.err = -1

    def get(self, name):             # get from memory stack current value of variable <name>
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem.get(name)
        return self.err

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        self.stack[-1].put(name, value)

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
