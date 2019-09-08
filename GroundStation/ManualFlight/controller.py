class controller(object):
    """description of class"""
    
    default_altitude = 10 # [m]
    jaw_delta = 10 # [deg]


    def __init__(self, mavcomm):
        self.gnd_speed = 5 # [m/s]
        self.elev_speed = 1 # [m/s]
        self.mc = mavcomm
        self.history = []
        self.current_mode="ground"  # air, ground, mission

   
    #-- Key event function
    def key(self):
        if 't' in self.history:
            if self.current_mode == "ground":
                print("t pressed ->> Takeoff")
                self.mc.arm_and_takeoff(controller.default_altitude)
                self.current_mode = "air" if self.mc.is_armed() else "ground"
                return

        if 'r' in self.history:
            if self.current_mode == "air":
                print("r pressed ->> Set the vehicle to RTL")
                self.mc.init_rtl()
                self.current_mode = "mission"
                return

        if 'space' in self.history:
            if self.current_mode == "mission":
                print("<space> pressed ->> Set the vehicle to Guided")
                self.mc.abort_rtl()                
                self.current_mode = "air" if self.mc.is_armed() else "ground"
                return

        if '1' in self.history:
            self.gnd_speed =  5 # 18 km/h
        elif '2' in self.history:
            self.gnd_speed = 10 # 36 km/h
        elif '3' in self.history:
            self.gnd_speed = 15 # 54 km/h
        elif '4' in self.history:
            self.gnd_speed = 20 # 72 km/h
        elif '5' in self.history:
            self.gnd_speed = 25 # 90 km/h

        self.mc.velocity_x = -self.gnd_speed if 'Down' in self.history else self.gnd_speed if 'Up' in self.history else 0
        self.mc.velocity_y = -self.gnd_speed if 'a' in self.history else self.gnd_speed if 'd' in self.history else 0
        self.mc.velocity_z = -self.elev_speed if 'w' in self.history else self.elev_speed if 's' in self.history else 0
    
        if 'Left' in self.history: # turn left            
            self.mc.jaw_angle -= controller.jaw_delta
            if self.mc.jaw_angle < 0:
                self.mc.jaw_angle += 360            
        elif 'Right' in self.history:  # turn right
            self.mc.jaw_angle += controller.jaw_delta
            if self.mc.jaw_angle > 360:
                self.mc.jaw_angle -= 360


    def keyup(self, event):
        if event.keysym in self.history :
            self.history.pop(self.history.index(event.keysym))
            self.key()


    def keydown(self, event):
        if not event.keysym in self.history :
            self.history.append(event.keysym)
            self.key()



