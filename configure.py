import odrive
from odrive.enums import *
from fibre.libfibre import ObjectLostError
from loguru import logger
from math import pi

#
def config_motor(odrv_num, axis_num, shouldClear, PSUChoice):

        #===================Reset=========================
        #If there were errors in the previous cycle, erase config would clear errors so you could start over
        odrv = odrive.find_any(serial_number=odrv_num)

        if shouldClear:
            try:
                odrv.erase_configuration()

            except ObjectLostError:
                pass

            odrv = odrive.find_any(serial_number=odrv_num)
            
            print("Erased Previous Configuration... 🗑️")
        #================================================

        axis = getattr(odrv, f'axis{axis_num}')
        
        #test function -- getting vbus_voltage to prove this is a unique odrive
        vbus_voltage = odrv.vbus_voltage
        print("Serial Number of connected odrive: ", odrv_num)
        print("VBUS_voltage of connected odrive: ", vbus_voltage)

        #=============ODRIVE CONFIGURATION===============
        #Need to be set to true if we are using a psu with a brake resistor
        
        if PSUChoice:
            odrv.config.enable_brake_resistor = True
            #maybe create new if in future if using different resistor (eg not 2ohms)
            odrv.config.brake_resistance = 2.0
        else:   
            odrv.config.enable_brake_resistor = False
            odrv.config.brake_resistance = 0.0
        #Odrivetool says the default value is 2.0 
        #(because the resitor that comes with the odrive is 50w 2ohm)
        #and to set it to default if not using br; look into this further.
        #If we are using a brake resistor change this value to resistor ohms.

        odrv.config.dc_bus_undervoltage_trip_level = 8.0
        odrv.config.dc_bus_overvoltage_trip_level = 56.0
        odrv.config.dc_max_positive_current = 40.0
        odrv.config.dc_max_negative_current = -20.0
        odrv.config.max_regen_current = 0
        #================================================

        #=============MOTOR CONFIGURATION================
        axis.motor.config.pole_pairs = 7
       
        axis.motor.config.resistance_calib_max_voltage = 5.0
        #axis.motor.config.resistance_calib_max_voltage = 20.0
        
        axis.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
        # axis.motor.config.motor_type = MOTOR_TYPE_GIMBAL
        
        # axis.motor.config.requested_current_range = 3.0
        # axis.motor.config.requested_current_range = 20.0

        axis.motor.config.current_lim_margin = 2.78
        
        axis.motor.config.current_control_bandwidth = 1000
        
        axis.motor.config.current_lim = 2.78
        # 473 is Kv of our neo motor. (Kv = RPM at max throttle)
        axis.motor.config.torque_constant = 0.114
        #================================================

        #================ENCODER CONFIGURATION====================
        #Can use ENCODER_MODE_HALL as found in odrive.enums
        axis.encoder.config.mode = ENCODER_MODE_HALL
        axis.encoder.config.cpr = 42
        #using an encoder with an index pin allows pre-calibration of the encoder and encoder index search
        #ours has index pins(Z) ; can set this to true
        axis.encoder.config.use_index = False
        #changed this to false, wasnt here before. default was true.
        axis.encoder.config.use_index_offset = False
        #Changed from true to false got illegalhallstate big surprise.
        #When trying to request closed loop state and set vel = 3 got the following errors
        #MotorError.UNKNOWN_TORQUE and MotorError.UNKNOWN_VOLTAGE_COMMAND
        #Set this value to true and all 3 errors went away and it spun ; further research needed.
        
        
        #axis.encoder.config.ignore_illegal_hall_state = True

        axis.encoder.config.calib_scan_distance = 4 * pi * 7
        
        axis.encoder.config.bandwidth = 350

        #=========================================================
        ##### cause motor to smoke ################
        axis.motor.config.calibration_current = 2.78
        ###########################################

        axis.config.calibration_lockin.current = 2.78
        axis.config.calibration_lockin.ramp_time = 0.4
        axis.config.calibration_lockin.ramp_distance = 3.1415927410125732
        axis.config.calibration_lockin.accel = 10
        axis.config.calibration_lockin.vel = 20

        # axis.controller.config.vel_limit = 90
        axis.controller.config.vel_limit = 10
        
        axis.controller.config.pos_gain = 1
        axis.controller.config.vel_gain = \
            0.02 * axis.motor.config.torque_constant * axis.encoder.config.cpr
        axis.controller.config.vel_integrator_gain = \
            0.1 * axis.motor.config.torque_constant * axis.encoder.config.cpr
        
        # axis.trap_traj.config.vel_limit = 30
        axis.trap_traj.config.accel_limit = 2
        axis.trap_traj.config.decel_limit = 2


        #===================================================================
        #               thermistor config
        #===================================================================
        axis.motor.motor_thermistor.config.enabled = True
        axis.motor.motor_thermistor.config.gpio_pin = 1
        
        # axis.motor.motor_thermistor.config.temp_limit_lower = 100
        # axis.motor.motor_thermistor.config.temp_limit_upper = 120

        #looked better with these values, not sure which to pick
        axis.motor.motor_thermistor.config.temp_limit_lower = 25
        axis.motor.motor_thermistor.config.temp_limit_upper = 85
        
        # NEEDS TO BE MANUALLY PUT IN ODRIVE TOOL
        #set_motor_thermistor_coeffs(odrv0.axis0, 5000, 5270, 3490, 25, 85)

        #===========================================================================
        #               double check
        #===========================================================================
            # In [5]: odrv0.axis0.motor.motor_thermistor.config.poly_coefficient_0
            # Out[5]: -647.2123413085938

            # In [6]: odrv0.axis0.motor.motor_thermistor.config.poly_coefficient_1
            # Out[6]: 833.781494140625

            # In [7]: odrv0.axis0.motor.motor_thermistor.config.poly_coefficient_2
            # Out[7]: -467.48223876953125

            # In [8]: odrv0.axis0.motor.motor_thermistor.config.poly_coefficient_3
            # Out[8]: 132.3001251220703



        #===================================================================
        axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH      #INPUT_MODE_VEL_RAMP
        axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

        # saving the new configuration
        print("Saving manual configuration and rebooting...")
        try:
            odrv.save_configuration()

        except ObjectLostError:
            pass
        print("Manual configuration saved.")
        
        #stupid