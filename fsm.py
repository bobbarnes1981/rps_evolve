
# first state 3 bits
# first ouptu 1 char
# *24
# implied 3 bits state
# implied 1 char input
# 3 bits next state
# 1 char output

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

#DEBUG
#b = fsm(last_input)
#print(b.get_output("R"))
#print(b.get_output("P"))
#print(b.get_output("S"))

