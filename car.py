import vesc
import time

class Car:
    def __init__(self, starting_state, debug, name="Mario") -> None:
        self.states = ["DEFAULT", "FOLLOW", "STOP", "R-UTURN", "L-UTURN", "RTURN", "LTURN"]
        self.name = name
        self.state = starting_state
        self.debug = debug
        self.vesc = vesc.VESC("/dev/ttyACM0")
        self.throttle = 0.0
        self.angle = 0.5
        
        # self.camera or whatever
    def default(self):
        self.vesc.run(0.5, 0.1)
        self.throttle = 0.1
        self.angle = 0.5
        if (self.debug):
            print("default")
    
    def stop(self):
        self.vesc.run(0.5, 0.0)
        self.throttle = 0.0
        self.angle = 0.5
        if (self.debug):
            print("stopping")
    
    def rturn(self):
        self.vesc.run(0.8, self.throttle)
        self.throttle = self.throttle
        self.angle = 0.8
        if (self.debug):
            print("right turn")
    
    def lturn(self):
        self.vesc.run(0.2, self.throttle)
        self.throttle = self.throttle
        self.angle = 0.2
        if (self.debug):
            print("left turn")
    
    def set_throttle(self, throttle):
        self.vesc.run(self.angle, throttle)
        self.throttle = throttle
        self.angle = self.angle
        if (self.debug):
            print("throttle set to ", throttle)
    
    def up_throttle(self):
        self.set_throttle(self.throttle + 0.05)
        if (self.debug):
            print("upped throttle")
    
    def down_throttle(self):
        self.set_throttle(self.throttle - 0.05)
        if (self.debug):
            print("downed throttle")

    def r_uturn(self):
        self.stop()
        self.vesc.run(0.4, 0.1)
        time.sleep(0.2)
        self.vesc.run(0.9, 0.1)
        time.sleep(0.6)
    
    def l_uturn(self):
            self.stop()
            self.vesc.run(0.6, 0.1)
            time.sleep(0.2)
            self.vesc.run(0.1, 0.1)
            time.sleep(0.6)
                
    def run(self):
        while True:
            # do camera stuff, but we'll ignore that for now
            new_state = input("state please\n")
            # error check the new state TODO

            if (new_state == "DEFAULT"):
                self.default()
            elif (new_state == "STOP"):
                self.stop()
            elif (new_state == "RTURN"):
                self.rturn()
            
            if (new_state == "w"):
                self.default()
            elif (new_state == "s"):
                self.stop()
            elif (new_state == "d"):
                self.rturn()
            elif (new_state == "a"):
                self.lturn()
            elif (new_state == "e"):
                self.up_throttle()
            elif (new_state == "q"):
                self.down_throttle()
            elif (new_state == "1"):
                self.l_uturn()
            elif (new_state == "2"):
                self.r_uturn()

