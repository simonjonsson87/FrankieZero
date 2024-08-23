#!/usr/bin/python
# coding=utf-8
# "DATASHEET": http://cl.ly/ekot   x.encode('hex') to codecs.encode(x)
from __future__ import print_function
import serial, struct, sys, time, codecs



class SimonsSDS011:

    DEBUG = 0x1
    CMD_MODE = 0x2
    CMD_QUERY_DATA = 0x4
    CMD_DEVICE_ID = 0x5
    CMD_SLEEP = 0x6
    CMD_FIRMWARE = 0x7
    CMD_WORKING_PERIOD = 0x8
    MODE_ACTIVE = 0x0
    MODE_QUERY = 0x1

    byte, data = 0, ""

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/serial0'
        self.ser.baudrate = 9600
        self.ser.parity=serial.PARITY_NONE
        self.ser.stopbits=serial.STOPBITS_ONE
        self.ser.bytesize=serial.EIGHTBITS
        self.ser.timeout=5

        self.ser.open()
        self.ser.flushInput()

        print("Opened serial connection")  

        self.cmd_set_sleep(0)
        self.cmd_set_mode(1)

        print("Initialised SDS011")
		
    def __del__(self):
        self.ser.close()
        print("Closed serial connection")
                

    def getReading(self):
         if self.ser.is_open:
            return self.cmd_query_data()
         else:
            print("Sorry, the serial connection to SDS011 appears to be closed.")   


    def dump(self, d, prefix=''):
        print(prefix + ' '.join(str(hex(x)) for x in d))


    def dump_array(self, d, prefix=''):
            print(prefix + ' '.join(str(x) for x in d))      

    def construct_command(self, cmd, data=[]):
        #print("=== construct_command  ===")
        assert len(data) <= 12
        data += [0x0,]*(12-len(data))
        checksum = (sum(data)+cmd-2)%256
        ret = [0xAA, 0xB4, cmd] + data + [0xFF, 0xFF, checksum, 0xAB]
        ret = bytes(ret)
        #for r in ret:
        #     print("type= " + str(type(r)))
        #     print(r)

        if self.DEBUG:
            self.dump_array(ret, '> ')
        return ret


    def process_data(self, d):
        print("=== process_data  ===")
        print("len(d) = " + str(len(d)))
        r = struct.unpack('<HHxxBB', d[2:])
        print(r)
        pm25 = r[0]/10.0
        pm10 = r[1]/10.0
        checksum = sum(v for v in d[2:8])%256
        print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
        s = 0 
        if checksum==r[2] and r[3]==0xab:
            s = "OK"
        else: 
            s = "NOK"
        return pm25, pm10, s


    def read_response(self):
        #print("--  read_response  --")
        byte = 0
        while byte != b'\xaa':
            byte = self.ser.read(size=1)
            print(byte)

        d = self.ser.read(size=9)

        if self.DEBUG:
            self.dump(d, '< ')
        return byte + d

    def cmd_set_mode(self, mode=MODE_QUERY):
        print("=== cmd_set_mode  ===")
        self.ser.write(self.construct_command(self.CMD_MODE, [0x1, mode]))
        self.read_response()

    def cmd_query_data(self):
        #print("=== cmd_query_data  ===")
        self.ser.write(self.construct_command(self.CMD_QUERY_DATA))
        d = self.read_response()
        #print("read_response result = " + str(d))
        #print(chr(d[1]))
        if chr(d[1]) == '\xc0':
            #print("Aperently d[1] == b'\xc0' and we are going to process_data")
            return self.process_data(d)

    def cmd_set_sleep(self, sleep=1):
        #print("=== cmd_set_sleep  ===")
        mode = 0x0 if sleep else 0x01
        self.ser.write(self.construct_command(self.CMD_SLEEP, [0x1, mode]))
        self.read_response()



