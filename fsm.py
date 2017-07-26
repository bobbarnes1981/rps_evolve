
# first state 3 bits
# first ouput 1 char
# *24
# implied 3 bits state
# implied 1 char input
# 3 bits next state
# 1 char output

# 4 * 25 = 100

# starting state XXX
# first output   X
# state in next out
# 000   R  XXX  X
# 000   P  XXX  X
# 000   S  XXX  X
# 001   R  XXX  X
# 001   P  XXX  X
# 001   S  XXX  X
# 010   R  XXX  X
# 010   P  XXX  X
# 010   S  XXX  X
# 011   R  XXX  X
# 011   P  XXX  X
# 011   S  XXX  X
# 100   R  XXX  X
# 100   P  XXX  X
# 100   S  XXX  X
# 101   R  XXX  X
# 101   P  XXX  X
# 101   S  XXX  X
# 110   R  XXX  X
# 110   P  XXX  X
# 110   S  XXX  X
# 111   R  XXX  X
# 111   P  XXX  X
# 111   S  XXX  X

# example genome that just outputs the previous input
#last_input = "000R000R000P000S000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R000R"
last_input = "xxxGENOMExxx"

class fsm(object):
    def __init__(self, config):
        self.map = [
            "R",
            "P",
            "S"
        ]
        self.config = config
        self.current_state = self.start_state()
    def start_state(self):
        return self.read_bits(0, 3)
    def start_output(self):
        return self.config[3]
    def read_bits(self, start, length):
        num = 1
        total = 0
        for i in range(length-1, -1, -1):
            total += int(self.config[start+i]) * num
            num = num * 2
        return total
    def get_output(self, input):
        #print 'input: ',input
        if input != "":
            input_id = self.map.index(input)
        else:
            input_id = self.map.index(self.start_output())
        #print 'input id: ',input_id
        index = 4 + (self.current_state * 12) + (input_id * 4)
        #print 'state: ',self.current_state
        #print 'offset: ',index
        self.current_state = self.read_bits(index, 3)
        #print 'new state: ',self.current_state
        output = self.config[index+3]
        #print 'output: ',output
        return output

if input == "":
    bot = fsm(last_input)

output = bot.get_output(input)

