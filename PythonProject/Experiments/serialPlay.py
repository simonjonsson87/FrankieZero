import serial
import struct

def dump(d, prefix=''):
        #print(prefix + ' '.join(str(bytes(x, 'utf-8').hex()) for x in d))
        print(prefix + ' '.join(hex(x) for x in d))

def read_response():
    #print("--  read_response  --")
    byte = 0
    while byte != b'\xaa':
        byte = ser.read(size=1)

    d = ser.read(size=9)

    dump(d, '< ')
    return byte + d



ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

try:
    print(ser.isOpen())
    #thestring = "\xC2\xAA\xC2\xB4\x06\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xC3\xBF\xC3\xBF\x06\xC2\xAB"
    #c2aa c2b4 06 01 01 00 00 00 00 00 00 00 00 00 00 c3bf c3bf 06 c2ab
    #data = struct.pack(hex(thestring))

    #               Start       Cmd     Data (12 bytes)                                                         After       Checksum    End
    data = bytes([  0xAA, 0xB4, 0x06,   0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06,       0xAB])
    #data = bytes([0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC3, 0xBF, 0xC3, 0xBF, 0x06, 0xC2, 0xAB])
    ser.write(data)
    read_response()
    #s = ser.read(9)
    #print(s)
    #print(' '.join(str(bytes(x, 'utf-8').hex()) for x in s))
finally:    
    ser.close()

