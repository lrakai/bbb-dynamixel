""" Test module """

import serial, fcntl, struct, time, sys, commands

def test():
	""" Test to blink LED and rotate motor """
	PRINT_PACKETS = 1 # 1 print packets sent and recieved, 0 disable printing packets
	ID = 0x01 # dynamixel id of rx-24f servo (can be found from wizard, or read data instruction)

	ser = serial.Serial(
		port='/dev/ttyO4', 
		baudrate=57600,  # baud rate can be set in the wizard
		timeout=1,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
	)

	# Standard Linux RS485 ioctl:
	TIOCSRS485 = 0x542F

	# define serial_rs485 struct per Michael Musset's patch that adds gpio RE/DE 
	# control:
	# (https://github.com/RobertCNelson/bb-kernel/blob/am33x-v3.8/patches/fixes/0007-omap-RS485-support-by-Michael-Musset.patch#L30)
	SER_RS485_ENABLED		  = (1 << 0)
	SER_RS485_RTS_ON_SEND	  = (1 << 1)
	SER_RS485_RTS_AFTER_SEND  = (1 << 2)
	SER_RS485_RTS_BEFORE_SEND = (1 << 3)
	SER_RS485_USE_GPIO		  = (1 << 5)

	# Enable RS485 mode using a GPIO pin to control RE/DE: 
	RS485_FLAGS = SER_RS485_ENABLED | SER_RS485_USE_GPIO 
	# With this configuration the GPIO pin will be high when transmitting and low
	# when not

	# If SER_RS485_RTS_ON_SEND and SER_RS485_RTS_AFTER_SEND flags are included the
	# RE/DE signal will be inverted, i.e. low while transmitting

	# The GPIO pin to use, using the Kernel numbering: 
	RS485_RTS_GPIO_PIN = 48 # GPIO1_16 -> GPIO(1)_(16) = (1)*32+(16) = 48

	# Pack the config into 8 consecutive unsigned 32-bit values:
	# (per  struct serial_rs485 in patched serial.h)
	serial_rs485 = struct.pack('IIIIIIII', 
							RS485_FLAGS,		# config flags
							0,				  # delay in us before send
							0,				  # delay in us after send
							RS485_RTS_GPIO_PIN, # the pin number used for DE/RE
							0, 0, 0, 0		  # padding - space for more values 
							)

	# Apply the ioctl to the open ttyO4 file descriptor:
	fd=ser.fileno()
	fcntl.ioctl(fd, TIOCSRS485, serial_rs485)


	# GPIO1_16 should be low here
	time.sleep(0.2)
	# GPIO1_16 should be high while this is being transmitted:

	# flash led to signal connection established
	blinkCount = 0
	ledOn = 0
	while blinkCount < 8:
		ledOn = (ledOn + 1) % 2
		commandSetLED(ser, ID, ledOn)
		time.sleep(0.125)
		blinkCount += 1

	# move to full clockwise and counterclockwise and back to the center
	commandSetSpeed(ser, ID, 100)
	time.sleep(0.25)
	commandSetGoal(ser, ID, 0)
	time.sleep(2.0)
	commandSetSpeed(ser, ID, 0)
	commandSetGoal(ser, ID, 1023)
	time.sleep(0.25)
	commandSetGoal(ser, ID, 512)
	time.sleep(0.25)

	# enter goal positions
	print 'Enter integer goal positions followed by enter.  Press x to exit'
	while True:
		line = sys.stdin.readline()
		try:
			goal = int(line)
			commandSetGoal(ser, ID, goal)
		except:
			if line.startswith('x'):
				print 'Exiting'
				break
			print 'Invalid input (integers or x only)'


	# GPIO1_16 should be low again after transmitting
	time.sleep(0.2)
	ser.close()