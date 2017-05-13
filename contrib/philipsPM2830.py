"""

Python Interchangeable Virtual Instrument Library

philipsPM2830.py
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

class philipsPM2830(philipsPM2800):
    "Philips/Fluke Linear PM2830 series IVI DC power supply driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(philipsPM2830, self).__init__(*args, **kwargs)

        # PM283x series comes in singles and doubles only
        self._output_count = 2

        # Available output modules for the PM283x series
        self._output_spec = [
            {
                'range': {
                    'P8V': (8.0, 15.0)
                },
                'ovp_max': 10.0,
                'ocp_max': 15.1,
                'voltage_max': 8.0,
                'current_max': 15.0
                
            },
            {
                'range': {
                    'P60V': (60.0, 2.0)
                },
                'ovp_max': 62.0,
                'ocp_max': 2.1,
                'voltage_max': 60.0,
                'current_max': 2.0
            },
            {
                'range': {
                    'P120V': (120.0, 1.0)
                },
                'ovp_max': 122.0,
                'ocp_max': 1.1,
                'voltage_max': 120.0,
                'current_max': 1.0
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
        self._identity_supported_instrument_models = ['PM2831', 'PM2832']
        
        self._init_outputs()
        

    
