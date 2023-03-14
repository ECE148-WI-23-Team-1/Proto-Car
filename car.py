import vesc
import time
import numpy as np  # numpy - manipulate the packet data returned by depthai
import cv2  # opencv - display the video stream
import depthai  # depthai - access the camera and its data packets
import blobconverter  # blobconverter - compile and download MyriadX neural network blobs
import camera

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
        with depthai.Device(pipeline) as device:
            # step 7
            q_rgb = device.getOutputQueue("rgb")
            q_nn = device.getOutputQueue("nn")

            # Output queue will be used to get the disparity frames from the outputs defined above
            q_depth = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
            
            # step 8
            frame = None
            detections = []

    # step 10
            while True:
                # step 11
                in_rgb = q_rgb.tryGet()
                in_nn = q_nn.tryGet()
                in_disparity = q_depth.get()

                #step 12
                if in_rgb is not None:
                    frame = in_rgb.getCvFrame()
                # step 13
                if in_nn is not None:
                    detections = in_nn.detections
                if in_disparity is not None:
                    depths = in_disparity.getCvFrame()
                
                print(np.shape(depths))
                #depths = depths[200:500,20:320]
                cv2.circle(depths, (285,215), 2, (255,255,255), 2)
                cv2.circle(depths, (285,265), 2, (255,255,255), 2)

                cv2.imshow("disparity", depths)
                #step 14
                if frame is not None:
                    for detection in detections:
                        bbox = camera.frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
                        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
                        cv2.circle(frame, (150,150), 2, (255,255,255), 2)
                        cv2.circle(frame, (150,200), 2, (255,255,255), 2)

                        if (detection.label == 15):
                            print("I found a... human...")
                        else:
                            print("Not a ... human ...")
                    cv2.imshow("preview", frame)
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

