"""

Python Interchangeable Virtual Instrument Library

philipsBaseDCPwr.py
Copyright (c) 2017 Coburn Wightman

Derived from rigolBaseDCPwr.py 
Copyright (c) 2013-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .. import ivi
from .. import dcpwr
from .. import scpi

TrackingType = set(['floating'])
TriggerSourceMapping = {
        'immediate': 'imm',
        'bus': 'bus'}

#class philipsBaseDCPwr(scpi.dcpwr.Base, scpi.dcpwr.Trigger, scpi.dcpwr.SoftwareTrigger, scpi.dcpwr.Measurement):
class philipsBaseDCPwr(scpi.dcpwr.Base, scpi.dcpwr.Measurement):
    "Philips generic IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(philipsBaseDCPwr, self).__init__(*args, **kwargs)
        
        self._output_count = 3
        
        self._output_spec = [
            {
                'range': {
                    'P30V': (30.0, 10.0)
                },
                'ovp_max': 32.0,
                'ocp_max': 10.1,
                'voltage_max': 30.0,
                'current_max': 10.0,
                'power_max' : 60
                
            },
            {
                'range': {
                    'P60V': (60.0, 5.0)
                },
                'ovp_max': 62.0,
                'ocp_max': 5.1,
                'voltage_max': 60.0,
                'current_max': 5.0,
                'power_max' : 60
            },
            {
                'range': {
                    'P60V': (60.0, 10.0)
                },
                'ovp_max': 62.0,
                'ocp_max': 10.1,
                'voltage_max': 60.0,
                'current_max': 10.0,
                'power_max' : 120
            }
        ]
        
        self._memory_size = 10
        
        self._identity_description = "Philips/Fluke generic IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Philips NV"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PM2810', 'PM2830']
        
        self._add_method('memory.save',
                        self._memory_save)
        self._add_method('memory.recall',
                        self._memory_recall)

        dcpwr.OutputState.add('over_temp')
        dcpwr.OutputState.add('sense_fail')
        dcpwr.OutputState.add('invalid_calibration')
        
        self._init_outputs()

    def _get_bool_str(self, value):
        """
        redefining to change behavior from '0'/'1' to 'off'/'on'
        """
        if bool(value):
            return 'on'
        return 'off'
    
    def _memory_save(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*sav %d" % index)
    
    def _memory_recall(self, index):
        index = int(index)
        if index < 1 or index > self._memory_size:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write("*rcl %d" % index)

    def _utility_self_test(self):
        code = 0
        message = "No Response"
        if not self._driver_operation_simulate:
            self._write("*TST?")
            # wait for test to complete
            message = self._read()
            if 'FAIL' in message:
                code = -1
        return (code, message)

    def _output_reset_output_protection(self, index):
        index = int(index)
        if index < 0 or index > self._output_count:
            raise OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":INST:NSEL %d" % index)
            self._write(":OUTP:PROT:CLE")
        return

    def _output_query_output_state(self, index, state):
        index = ivi.get_index(self._output_name, index)
        if state not in dcpwr.OutputState:
            raise ivi.ValueNotSupportedException()
        oper_status = 0
        ques_status = 0
        if not self._driver_operation_simulate:
            oper_status = int(self._ask("stat:oper:inst:isum%d:cond?" % (index+1)))
            ques_status = int(self._ask("stat:ques:inst:isum%d:cond?" % (index+1)))
        if state == 'constant_voltage':
            return oper_status & (1 << 8) != 0
        elif state == 'constant_current':
            return oper_status & (1 << 9) != 0
        elif state == 'over_voltage':
            return ques_status & (1 << 0) != 0
        elif state == 'over_current':
            return ques_status & (1 << 1) != 0
        elif state == 'over_temp':
            return ques_status & (1 << 4) != 0
        elif state == 'sense_fail':
            return ques_status & (1 << 4) != 0
        elif state == 'invalid_calibration':
            return ques_status & (1 << 8) != 0
        elif state == 'unregulated':
            return ques_status & (275) != 0
            
        return False

