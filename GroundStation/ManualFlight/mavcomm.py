import time
from pymavlink import mavutil
from dronekit import connect, VehicleMode #, LocationGlobalRelative, Command, LocationGlobal


class mavcomm:
    """MAVLink communication class"""
    
    def __init__(self, ip):
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.jaw_angle = 0
        self.stop = False
    
        #-- Connect to the vehicle
        print(f'Connecting to {ip}...')
        self.vehicle = connect(ip, wait_ready=True)  # accept UDP from ip
       

    #-- Define the function for sending mavlink velocity command in body frame
    def set_velocity_body(self):
        """ Remember: vz is positive downward!!!
        http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html
    
        Bitmask to indicate which dimensions should be ignored by the vehicle 
        (a value of 0b0000000000000000 or 0b0000001000000000 indicates that 
        none of the setpoint dimensions should be ignored). Mapping: 
        bit 1: x,  bit 2: y,  bit 3: z, 
        bit 4: vx, bit 5: vy, bit 6: vz
        """
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
                0, # time_boot_ms (not used)
                0, 0, # target_system, target_component
                mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
                0b0000111111000111, #-- BITMASK -> Consider only the velocities
                0, 0, 0,        #-- POSITION
                self.velocity_x, self.velocity_y, self.velocity_z,     #-- VELOCITY
                0, 0, 0,        #-- ACCELERATIONS (not supported yet, ignored in GCS_Mavlink)
                0, 0) 			# yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        # send command to vehicle
        self.vehicle.send_mavlink(msg)        
    

    #-- Define the function for sending mavlink condition jaw command
    def set_condition_yaw(self, relative=False):
        if relative:
            is_relative=1 #yaw relative to direction of travel
        else:
            is_relative=0 #yaw is an absolute angle
        # create the CONDITION_YAW command using command_long_encode()
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,           # target system, target component
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0,              #confirmation
            self.jaw_angle, # param 1, yaw in degrees
            0,              # param 2, yaw speed deg/s
            1,              # param 3, direction -1 ccw, 1 cw
            is_relative,    # param 4, relative offset 1, absolute angle 0
            0, 0, 0)        # param 5 ~ 7 not used
        # send command to vehicle
        self.vehicle.send_mavlink(msg)


    #-- Define arm and takeoff
    def arm_and_takeoff(self, altitude):
        if self.vehicle.armed == False:
            retry = 0
            while not self.vehicle.is_armable:
                print("waiting to be armable")            
                time.sleep(1)
                retry += 1
                if retry > 5:
                    return False

            print("Arming motors")
            self.vehicle.mode = VehicleMode("GUIDED")
            self.vehicle.armed = True
            retry = 0
            while not self.vehicle.armed:
                time.sleep(1)
                retry += 1
                if retry > 5:
                    return False

        print("Taking Off")
        self.vehicle.simple_takeoff(altitude)

        retry = 0
        while True:
            v_alt = self.vehicle.location.global_relative_frame.alt
            print(">> Altitude = %.1f m"%v_alt)
            if v_alt >= altitude - 1.0:
                print("Target altitude reached")
                return True
            time.sleep(1)
            retry += 1
            if retry > 10:
                return False
    

    def init_rtl(self):
        self.vehicle.mode = VehicleMode("RTL")


    def abort_rtl(self):
        self.vehicle.mode = VehicleMode("GUIDED")


    @property
    def armed(self):
        return self.vehicle.armed


    # the background command loop
    def send_command(self):
        while not self.stop: 
            self.set_velocity_body()
            self.set_condition_yaw()
            self.vehicle.flush()
            time.sleep(1)

