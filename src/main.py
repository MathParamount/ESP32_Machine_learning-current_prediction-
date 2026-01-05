from regression import *

import serial as sr
import time

#Hardware informations
print('-- Hardware information --');

port = '/dev/ttyACM0'
while True:
    try:
        sensor = sr.Serial(port, 115200, timeout = 1)
        break
        
    except sr.SerialException:
        print(f"{port} busy, retrying...")
        time.sleep(1)

reader = reading(sensor)

#collecting enough samples 
for i in range(0,39):
    adc_value_read = reader.read_data()
    print(f"{adc_value_read}")
    time.sleep(0.2)
    
print("\n Dataframe collected\n")

reader.read_data()

reader.visualization_plot()

print('------------------------------');

#Machine learning prediction

print('-- Perceptron regression --');
    
if len(adc_value_read) < 2:
    print("ERROR: You Collected less than 2 samples!")
    print("You should verify the connection with sensor.")
else:
    # Machine learning tentative
    try:
        reg = regression(reader.get_dataframe())
        
        print(f"Coefficient (w): {np.round(reg.w,decimals=4)}")
        
        reg.visualization_reg()
        
    except ValueError as e:
        print(f"\nError in training model: {e}")
