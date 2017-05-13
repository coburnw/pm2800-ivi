# Toy to tinker with Philips/Fluke pm2800 power supply using Python-IVI
#
# BEWARE: runs supply up to 20 volts.  Be sure to have your lvcmos prototype disconnected.
#

import sys
import time

import ivi

##
## hit your instrument directly, bypassing IVI and the IVI driver
##

# import vxi11
# instr = vxi11.Instrument("192.168.2.9", "gpib0,5")
# print instr.ask("*IDN?")
# #print instr.ask(':stat:oper:cond?')
# oper = int(instr.ask(':stat:oper:inst:isum%d:cond?' % 1))
# ques = int(instr.ask(':stat:ques:inst:isum%d:cond?' % 1))
#
# quit()

##
## use IVI and the PM2800 driver to interact with a vxi-11 connected instrument.
##

def printstate():
    print ' Power Supply Enabled = ' + str(ps0.enabled)
    print ' Over Voltage Value = ' + str(ps0.ovp_limit)
    print ' Over Current Behavior = ' + ps0.current_limit_behavior
    print ' output voltage setting = ' + str(ps0.voltage_level)
    print ' output current setting = ' + str(ps0.current_limit)
    print '  present Constant Voltage state is: ' + str(ps0.query_output_state('constant_voltage'))
    print '  present Constant Current state is: ' + str(ps0.query_output_state('constant_current'))
    print '  present Over Voltage state is: ' + str(ps0.query_output_state('over_voltage'))
    print '  present Over Current state is: ' + str(ps0.query_output_state('over_current'))
    print '  present Unregulated state is: ' + str(ps0.query_output_state('unregulated'))    
    print '  measured output voltage = ' + str(ps0.measure('voltage'))
    print '  measured output current = ' + str(ps0.measure('current'))


if __name__ == '__main__':
    instr = ivi.contrib.philipsPM2811("TCPIP0::192.168.2.9::gpib0,5::INSTR")

    #instr.help()

    print instr.identity.description
    print instr.identity.instrument_manufacturer,
    print instr.identity.instrument_model,
    print ' has ' + str(len(instr.outputs)) + ' channels.'
    print instr.identity.instrument_firmware_revision
    print instr.identity.instrument_serial_number
    print instr.identity.supported_instrument_models
    print instr.identity.group_capabilities
    print instr.identity.identifier


    print 'Modules:'
    for i in range(len(instr.outputs)):
        print ' ' + instr.outputs[i].name
        print '  detecting limits'
        print '   ' + str(instr.outputs[i].query_voltage_level_max(0.0)) + ' max volts.'
        print '   ' + str(instr.outputs[i].query_current_limit_max(0.0)) + ' max amps.'
        print '  exploring capacity'
        print '   at ' + str(25) + ' volts, max current is ' + str(instr.outputs[i].query_current_limit_max(25.0)) + ' amps.'
        print '   at ' + str(5) + ' amps, max voltage is ' + str(instr.outputs[i].query_voltage_level_max(5.0)) + ' volts.'
        print '  calibration valid  ' + str(not instr.outputs[i].query_output_state('invalid_calibration'))

    ps0 = instr.outputs[0]
    ps0.enabled = False
    ps0.reset_output_protection()
        
    print
    print 'Simple test to exercise driver and device'
    print 'Test assumes a 5 watt 220 ohm load'

    ps0.ovp_limit = 20.0
    ps0.ovp_enabled = True

    print
    print 'testing constant current mode:'
    ps0.voltage_level = 10.0
    ps0.current_limit = 0.05
    ps0.current_limit_behavior = 'regulate'
    ps0.enabled = True
    time.sleep(1)
    printstate()
    ps0.enabled = False

    print
    print 'testing constant current mode:'
    ps0.voltage_level = 19.0
    ps0.current_limit = 0.05
    ps0.current_limit_behavior = 'regulate'
    ps0.enabled = True
    time.sleep(1)
    printstate()
    ps0.enabled = False

    print
    print 'testing over current trip:'
    ps0.voltage_level = 19.0
    ps0.current_limit = 0.05
    ps0.current_limit_behavior = 'trip'
    ps0.enabled = True
    time.sleep(1)
    printstate()
    ps0.voltage_level = 10
    ps0.enabled = False
    ps0.reset_output_protection()


    print
    print 'testing over voltage trip:'
    ps0.voltage_level = 21.0
    ps0.current_limit = 0.2
    ps0.current_limit_behavior = 'regulate'
    ps0.enabled = True
    time.sleep(1)
    printstate()
    ps0.voltage_level = 19.0
    ps0.enabled = False
    ps0.reset_output_protection()

