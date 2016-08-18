"""
Dynamixel Commands

Addresses can be found here:
http://support.robotis.com/en/product/dynamixel/rx_series/rx-24f.htm
"""

import instructions

def commandSetLED( ser, id, on ):
	""" 
	Set the state of the LED

	on = 1 turns LED on, on = 0 turns LED off 
	"""
	instructionWriteData(ser, id, [0x19, on])
	return

def commandSetGoal( ser, id, goal ):
	"""
	Set the motor goal position

	goal between 0 (maximum clockwise), and 1023 (maximum counterclockwise)
	only applies in joint mode
	"""
	if goal < 0:
		goal = 0
	elif goal > 1023:
		goal = 1023

	# split goal into lower and upper byte
	loGoal = goal & 0xff
	hiGoal = (goal >> 8) & 0xff	
	instructionWriteData(ser, id, [0x1e, loGoal, hiGoal])
	return

def commandSetSpeed( ser, id, speed ):
	"""
	Set motor moving speed

	speed between 1 (slowest) and 1023 (fastest, except 0)
	0 means maximum rpm without controlling speed
	"""
	if speed < 0:
		speed = 0
	elif speed > 1023:
		speed = 1023

	# split speed into lower and upper byte
	loSpeed = speed & 0xff
	hiSpeed = (speed >> 8) & 0xff
	instructionWriteData(ser, id, [0x20, loSpeed, hiSpeed])
	return