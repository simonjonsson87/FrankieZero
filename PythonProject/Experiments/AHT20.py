import adafruit_ahtx0
import board

# Setup I2C Sensor
sensor = adafruit_ahtx0.AHTx0(board.I2C())

# Convert Celsius to Fahrenheit 
def c_to_f(input):
    return (input * 9 / 5) + 32

# Convert to two decimal places cleanly
# round() won't include trailing zeroes
def round_num(input):
   return '{:.2f}'.format(input)

print('Temperature', round_num(sensor.temperature), 'C')
print('Humidity', round_num(sensor.relative_humidity), '%')