"""

Python Interchangeable Virtual Instrument Library

philipsPM2810.py
Copyright (c) 2017 Coburn Wightman

Derived from rigolDP800.py 
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

from .philipsPM2800 import *

class philipsPM2810(philipsPM2800):
    "Philips/Fluke Autoranging PM2810 series IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(philipsPM2810, self).__init__(*args, **kwargs)
        
        self._output_count = 3

        # Available output modules for the PM281x series
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
        
        #self._memory_size = 10
        
        self._identity_description = "Philips/Fluke Autoranging PM2810 series IVI DC power supply driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Philips NV"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['PM2811', 'PM2812', 'PM2813']
        
        self._init_outputs()
        

    # 281x are switchmode supplies therefore power limited 
    def _output_query_current_limit_max(self, index, voltage_level):
        index = ivi.get_index(self._output_name, index)
        if voltage_level < 0 or voltage_level > self._output_spec[index]['voltage_max']:
            raise ivi.OutOfRangeException()
        if voltage_level > 0:
            imax = self._output_spec[index]['power_max'] / voltage_level
            if imax > self._output_spec[index]['current_max']:
                imax = self._output_spec[index]['current_max']
        else:
            imax = self._output_spec[index]['current_max']
        return imax
    
    def _output_query_voltage_level_max(self, index, current_limit):
        index = ivi.get_index(self._output_name, index)
        if current_limit < 0 or current_limit > self._output_spec[index]['current_max']:
            raise ivi.OutOfRangeException()
        elif current_limit > 0:
            vmax = self._output_spec[index]['power_max'] / current_limit
            if vmax > self._output_spec[index]['voltage_max']:
                vmax = self._output_spec[index]['voltage_max']
        else:
            vmax = self._output_spec[index]['voltage_max']
        return vmax

    
