# MIT License
# 
# Copyright (c) 2018 Dan Persons <dpersonsdev@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from datetime import datetime
import time.timezone, time.altzone

class ParseModule:
    def __init__(self):
        """Initialize the standard syslog parsing module"""
        self.name = 'nohost'
        self.desc = 'syslog (without host) parsing module'
        self.date_format = \
                re.compile(r"^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\[?\d*\]?):")
        self.tzone = None

        # Set our timezone
        if not self.tzone:
            if time.localtime().tm_isdst:
                self.tzone = \
                        str(int(float(time.altzone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.altzone) / 60 % 60)).ljust(2, '0')
            else:
                self.tzone = \
                        str(int(float(time.timezone) / 60 // 60)).rjust(2,
                                '0') + \
                        str(int(float(time.timezone) / 60 % 60)).ljust(2, '0')
            if not '-' in self.tzone and not '+' in self.tzone:
                self.tzone = '+' + self.tzone
                        
    def parse_line(self, line):
        """Parse a syslog line (with standard BSD timestamp) into a dictionary"""
        match = re.findall(self.date_format, line)
        if match:
            attr_list = str(match[0]).split(' ')
            try:
                attr_list.remove('')
            except ValueError:
                pass

            # Put the date stamp back together
            datestamp = ' '.join(attr_list[0], attr_list[1], attr_list[2])

            # Set our attributes:
            sourceproclist = attr_list[3].split('[')
            if len(sourceproclist) > 1:
                sourcepid = sourceproclist[1].strip(']')
            else: sourcepid = None
            
            entry = {}


            entry['date_stamp'] = datestamp
            entry['time_zone'] = self.tzone
            entry['facility'] = None
            entry['severity'] = None
            entry['source_host'] = None
            entry['source_port'] = None
            entry['source_process'] = sourceproclist[0]
            entry['source_pid'] = sourcepid
            entry['dest_host'] = None
            entry['dest_port'] = None
            entry['protocol'] = None
            entry['message'] = line[len(match[0]) + 2:]

            return entry
        

        else: return None