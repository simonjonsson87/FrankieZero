#!/usr/bin/python
# coding=utf-8
# "DATASHEET": http://cl.ly/ekot   x.encode('hex') to codecs.encode(x)
from __future__ import print_function
import serial, struct, sys, time, codecs

DEBUG = 0x1
CMD_MODE = 0x2
CMD_QUERY_DATA = 0x4
CMD_DEVICE_ID = 0x5
CMD_SLEEP = 0x6
CMD_FIRMWARE = 0x7
CMD_WORKING_PERIOD = 0x8
MODE_ACTIVE = 0x0
MODE_QUERY = 0x1


ser = serial.Serial()
ser.port = '/dev/serial0'
ser.baudrate = 9600
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.bytesize=serial.EIGHTBITS
ser.timeout=5

ser.open()
ser.flushInput()

byte, data = 0, ""

def str2hex(x):
    #print("------ START -------")
    #print(type(x))
    #print(x)
    #print(bytearray(x, encoding='utf-8'))
    #print(len(x))
    #print("-------- END -------")
    return str(bytes(x, 'utf-8').hex())

    an_integer = int(x, 16)
    hex_value = hex(an_integer)
    return hex_value

def dump(d, prefix=''):
    #print(bytes(d, 'utf-8').hex())
    print(prefix + ' '.join(str(hex(x)) for x in d))
    #print(prefix + ' '.join(x.encode('hex') for x in d))

def dump2(d, prefix=''):
        print(prefix + ' '.join(str(bytes(x, 'utf-8').hex()) for x in d))

def dump_array(d, prefix=''):
        print(prefix + ' '.join(str(x) for x in d))      

def construct_command(cmd, data=[]):
    #print("=== construct_command  ===")
    assert len(data) <= 12
    data += [0x0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = [0xAA, 0xB4, cmd] + data + [0xFF, 0xFF, checksum, 0xAB]
    ret = bytes(ret)
    #for r in ret:
    #     print("type= " + str(type(r)))
    #     print(r)

    if DEBUG:
        dump_array(ret, '> ')
    return ret

def construct_command_LEGACY(cmd, data=[]):
    #print("=== construct_command  ===")
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret


def process_data(d):
    print("=== process_data  ===")
    print("len(d) = " + str(len(d)))
    r = struct.unpack('<HHxxBB', d[2:])
    print(r)
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(v for v in d[2:8])%256
    print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))

def process_version(d):
    print("=== process_version  ===")
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    #print("--  read_response  --")
    byte = 0
    while byte != b'\xaa':
        byte = ser.read(size=1)
        print(byte)

    #d = b''
    #for i in range(1,9):
    #    byte = ser.read(size=1)
    #    print(byte)
    #    d += byte

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    print("=== cmd_set_mode  ===")
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_set_mode_no_wait(mode=MODE_QUERY):
    print("=== cmd_set_mode  ===")
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    time.sleep(3)    

def cmd_query_data():
    print("=== cmd_query_data  ===")
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    print("read_response result = " + str(d))
    print(chr(d[1]))
    if chr(d[1]) == '\xc0':
        print("Aperently d[1] == b'\xc0' and we are going to process_data")
        process_data(d)

def cmd_set_sleep(sleep=1):
    print("=== cmd_set_sleep  ===")
    mode = 0x0 if sleep else 0x01
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_sleep_no_wait(sleep=1):
    print("=== cmd_set_sleep  ===")
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    time.sleep(3)   

def cmd_set_working_period(period):
    print("=== cmd_set_working_period  ===")
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    print("=== cmd_firmware_ver  ===")
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    print("=== cmd_set_id  ===")
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()

if __name__ == "__main__":
    try:
        cmd_set_sleep(0)
        cmd_set_mode(1)
        #cmd_firmware_ver()
        time.sleep(3)

        #cmd_query_data()
        #cmd_set_mode(0)
        #cmd_set_sleep(1)
        
        while True:
            cmd_query_data()
            time.sleep(10)

    finally:
        ser.close()
        print("Closed connection")