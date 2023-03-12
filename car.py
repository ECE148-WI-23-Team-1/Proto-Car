import vesc

class Car:
    def __init__(self, starting_state, debug, name="Mario") -> None:
        self.states = ["DEFAULT", "FOLLOW", "STOP", "R-UTURN", "L-UTURN", "RTURN", "LTURN"]
        self.name = name
        self.state = starting_state
        self.debug = debug
        # self.vesc = vesc.VESC("/dev/tty/ACM0")
        # self.camera or whatever
    def default(self):
        #self.vesc.run(0.5, 0.1)
        if (self.debug):
            print("default")
    
    def stop(self):
        #self.vesc.run(0.5, 0.0)
        if (self.debug):
            print("stopping")
    
    def rturn(self):
        #self.vesc.run(0.8, 0.1)
        if (self.debug):
            print("right turn")
    
    def run(self):
        while True:
            # do camera stuff, but we'll ignore that for now
            new_state = input("state please")
            # error check the new state TODO

            if (new_state == "DEFAULT"):
                self.default()
            elif (new_state == "STOP"):
                self.stop(self)
            elif (new_state == "RTURN"):
                self.rturn(self)



