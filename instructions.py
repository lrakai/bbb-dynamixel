""" 
Dynamixel Instructions 
http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm
"""

import packet

def instructionPing( ser, id ):
	""" Ping instruction """
	p = makePacket(id, 0x01, [])
	sendPacket(ser, p)
	p = receivePacket(ser, id)
	return

def instructionWriteData( ser, id, params ):
	""" Write data instruction """
	p = makePacket(id, 0x03, params)
	sendPacket(ser, p)
	p = receivePacket(ser, id)
	return

def instructionRegWrite( ser, id, params ):
	""" Write register instruction """
	p = makePacket(id, 0x04, params)
	sendPacket(ser, p)
	p = receivePacket(ser, id)
	return

def instructionAction( ser, id ):
	""" Action instruction """
	p = makePacket(id, 0x05, [])
	sendPacket(ser, p)
	p = receivePacket(ser, id)
	return