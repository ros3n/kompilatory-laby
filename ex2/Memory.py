class Memory:


    def __init__(self, name): # memory name
        self.data = {}

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
        print "Memory.get not found"
        return self.err

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for mem in reversed(self.stack):
            if mem.has_key(name):
                mem.put(name, value)
                return

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
