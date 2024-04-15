# from machine import 
import RPi.GPIO as GPIO
import serial

#NPK Sensor set up
uart0 = serial.Serial(
	port='/dev/ttyUSB1',
	baudrate=4800,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)


nitro = bytes.fromhex('01 03 00 1e 00 01 e4 0c')
phos = bytes.fromhex('01 03 00 1f 00 01 b5 cc')
pota = bytes.fromhex('01 03 00 20 00 01 85 c0')

if uart0.write(nitro):
	print(uart0)
	Tx_Nitro = uart0.write(nitro)
	print("Sent Data : " + str(Tx_Nitro))
	Rx_Nitro = uart0.readline()
	print("Received data : " + str(Rx_Nitro))
	Nitrogen_Value = ((int.from_bytes(Rx_Nitro[3], 'big')) << 8) + (int.from_bytes(Rx_Nitro[4], 'big'))
	Rx_Nitro = uart0.read(7)
	print("Received data : " + str(Rx_Nitro))
else:
	print("No Data")

# Sensor response is in mg/kg
# def nitrogen():

	# n = 53
	# return n
	# convert value into kg/ha
	# if uart0.write(nitro):
	# 	Rx_Nitro = uart0.read(7)
 #        # print("Received data : " + str(Rx_Nitro))
 #        # Nitrogen_Value = int.from_bytes(Rx_Nitro[3:5], 'big')
 #        # return Nitrogen_Value
 #    else:
 #    	print("Data Didn't Transmit")

def phosphorus():
	p = 120
	return p
	# if uart0.write(phos):
 #        Rx_Phos = uart0.read(7)
 #        print("Received data : " + str(Rx_Phos))
 #        Phosphorus_Value = int.from_bytes(Rx_Phos[3:5], 'big')
 #        return Phosphorus_Value
 #    else:
 #        print("Data Didn't Transmit")

def potassium():
	k = 118
	return k
 	# if uart0.write(pota):
  #       Rx_Pota = uart0.read(7)
  #       print("Received data : " + str(Rx_Pota))
  #       Potassium_Value = int.from_bytes(Rx_Pota[3:5], 'big')
  #       return Potassium_Value
  #   else:
  #       print("Data Didn't Transmit")