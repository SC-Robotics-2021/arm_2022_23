import sys
import time
import odrive
from odrive.enums import *
from loguru import logger
from fibre.libfibre import ObjectLostError

def calib_motor(odrv_num, axis_num):
        #=======================================CALIBRATION SEQUENCE==============================================

        odrv = odrive.find_any(serial_number=odrv_num)

        axis = getattr(odrv, f'axis{axis_num}')

        #===============================================================
        #INPUT_MODE_PASSTHROUGH
        axis.controller.config.input_mode = 1   #INPUT_MODE_VEL_RAMP

        #CONTROL_MODE_VELOCITY_CONTROL
        axis.controller.config.control_mode = 2

        #===============================================================

        #THESE CALIBRATION STATES HAVE TO BE IN ORDER, ELSE IT WILL BE MEAN.



        #==============================MOTOR CALIBRATION=================================

        # MEASURING PHASE RESISTANCE/INDUCTANCE OF MOTOR
        # to store these values, do motor.config.pre_calibrated = True, as we do below.
        axis.requested_state = AXIS_STATE_MOTOR_CALIBRATION
        # Sleep to allow the motor to finish the calibrate process.
        print("OdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)
        
        print("OdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        
        
        # If there was an error during motor calibration, exit and link to error list.
        if axis.motor.error != 0:
            logger.error("Error at motor calibration 😢")
            print("Odrive: ", odrv_num, "Axis: ", axis_num)
            print(axis.motor.error)
            print("hold ctrl  v")
            # To regenerate this file, nagivate to the top level of the ODrive repository and run:
            # python Firmware/interface_generator_stub.py --definitions Firmware/odrive-interface.yaml --template tools/enums_template.j2 --output tools/odrive/enums.py
            print("https://github.com/odriverobotics/ODrive/blob/master/tools/odrive/enums.py")
            sys.exit()

        #================================================================================

        #================================ENCODER CALIBRATION===============================
        # This stores motor.config.phase_resistance and motor.config.phase_inductance to the odrive memory.
        logger.debug("Setting motor to precalibrated... 😎️")
        axis.motor.config.pre_calibrated = True
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)

        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        time.sleep(5)
        

        # Rotate the motor in lockin and calibrate hall polarity
        logger.debug("Calibrating Hall Polarity... 🤞")
        axis.requested_state = AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)

        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        time.sleep(5)

        # If there was an error during encoder polarity calibration, exit and link to error list.
        if axis.encoder.error != 0:
            logger.error("Error at Calibrating Hall Polarity 😢")
            print(axis.encoder.error)
            print("hold ctrl  v")
            # To regenerate this file, nagivate to the top level of the ODrive repository and run:
            # python Firmware/interface_generator_stub.py --definitions Firmware/odrive-interface.yaml --template tools/enums_template.j2 --output tools/odrive/enums.py
            print("https://github.com/odriverobotics/ODrive/blob/master/tools/odrive/enums.py")
            sys.exit()


        # Rotate the motor for 30s to calibrate hall sensor edge offsets
        # Note: The phase offset is not calibrated at this time, so the map is only relative
        logger.debug("Calibrating Hall Phase... 🤞")
        axis.requested_state = AXIS_STATE_ENCODER_HALL_PHASE_CALIBRATION
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)
        
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        time.sleep(5)

        # If there was an error during encoder phase calibration, exit and link to error list.
        if axis.encoder.error != 0:
            logger.error("Error at Calibrating Hall Phase 😢")
            print(axis.encoder.error)
            print("hold ctrl")
            # To regenerate this file, nagivate to the top level of the ODrive repository and run:
            # python Firmware/interface_generator_stub.py --definitions Firmware/odrive-interface.yaml --template tools/enums_template.j2 --output tools/odrive/enums.py
            print("https://github.com/odriverobotics/ODrive/blob/master/tools/odrive/enums.py")
            sys.exit()

        


        # Turns the motor in one direction for a few seconds and then back to measure the offset between the encoder position and the electrical phase.
        # Needs motor to be calibrated
        # If successful, encoder calibration will make the encoder.is_ready == True
        logger.debug("Calibrating Hall Offset... 🤞")
        axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)

        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        time.sleep(5)

        # If there was an error during encoder offset calibration, exit and link to error list.
        if axis.encoder.error != 0:
            logger.error("Error at Calibrating Hall Offset 😢")
            print(axis.encoder.error)
            print("hold ctrl")
            # To regenerate this file, nagivate to the top level of the ODrive repository and run:
            # python Firmware/interface_generator_stub.py --definitions Firmware/odrive-interface.yaml --template tools/enums_template.j2 --output tools/odrive/enums.py
            print("https://github.com/odriverobotics/ODrive/blob/master/tools/odrive/enums.py")
            sys.exit()



        logger.debug("Setting encoder to precalibrated... 😎️")
        axis.encoder.config.pre_calibrated = True
        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        while axis.current_state != AXIS_STATE_IDLE:
            time.sleep(2)

        print("\nOdriveSN: ",odrv_num, "\nState: ", axis.current_state, "\nAxis: ", axis_num)
        time.sleep(5)

        logger.debug("trying to save...")
        # saving the new configuration
        print("Saving manual configuration and rebooting... 😎️")
        try:
            odrv.save_configuration()

        except ObjectLostError:
            pass
        print("Manual configuration saved.")
        logger.debug("saved...")

        odrv = odrive.find_any(serial_number=odrv_num)
        axis = getattr(odrv, f'axis{axis_num}')

        #==================================================================================

    
        #===================================RUN SEQUENCE===================================

                

        #==================================================================================

    #github sucks weiner