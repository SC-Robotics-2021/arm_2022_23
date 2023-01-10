# from klampt import IKObjective,IKSolver
# from klampt.model import ik

from callback_api import *
from src.odrives.calibrate import *
import src.controller.gamepad_input as gmi
import subprocess



AXIS_DEADZONE = 0.3 # Deadzone is 0 to 1 | Note: axis value will be 0 until you move past the deadzone
MIN_SPEED = -20
MAX_SPEED = 20
CREMENT = 5



def eventHandler(odrv_0, odrv_1=None):
    # obj = ik.objective(robotlink,local=localpt,world=worldpt)
    # solver = ik.solver(obj)

    buttonDownEvents = [
        north, west, south, east,
        share, options, home,                       
        l1, r1, l3, r3]

    buttonUpEvents = [
        northUp, westUp, southUp, eastUp, 
        shareUp, optionsUp, homeUp, 
        l1Up, r1Up, l3Up, r3Up]

    hatEvents = [hatNorth, hatSouth, hatWest, hatEast, hatCentered]                     # Set hat callbacks
    connectionEvents = [onGamepadConnect, onGamepadDisconnect]                          # Set connection callbacks
    gmi.run_event_loop(buttonDownEvents, buttonUpEvents, hatEvents, connectionEvents)   # Async loop to handle gamepad button events

    speed = 5

    while True:
        odrv0 = odrive.find_any(serial_number=odrv_0)       # Get odrive object
        if odrv_1:
            odrv1 = odrive.find_any(serial_number=odrv_1)   # Get odrive object

        gp = gmi.getGamepad(0)                              # Get gamepad object

        (ls_x, ls_y) = gmi.getLeftStick(gp, AXIS_DEADZONE)  # Get left stick
        (rs_x, rs_y) = gmi.getRightStick(gp, AXIS_DEADZONE) # Get right stick
        (l2, r2) = gmi.getTriggers(gp, AXIS_DEADZONE)       # Get triggers
        (hat_x, hat_y) = gmi.getHat(gp)                     # Get hat
        
        if gmi.getButtonValue(gp, 1):
            ...

        
        




if __name__ == "__main__":
    odrives = get_all_odrives()
    # Odrive 0:  366B385A3030 
    # Odrive 1:  365F385E3030
    odrv0 = odrives[0]
    odrv1 = odrives[1]

    calibrate_all_motors(odrv0, odrv1)
    eventHandler(odrv_0=odrv0, odrv_1=odrv1)
    