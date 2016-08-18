""" Serial communication primitives """

import array

# PRINT_PACKETS = 1 # uncomment to print packets sent and received

def makePacket( id, instruction, params ):
	""" Make a dynamixel formatted packet """
	p = [
		0xff,
		0xff,
		id & 0xff,
		len(params)+2,
		instruction & 0xff
	]
	for param in params:
		p.append(param & 0xff)
	p.append(checksumPacket(p))
	return p

def checksumPacket( p ):
	""" Calculate the checksum byte for the packet """
	sum = 0
	for byte in p[2:]:
		sum = 0xff & (sum + byte)
	notSum = 0xff & (~sum)
	return notSum
 
def checkPacket( id, p ):
	""" 
	check bytes for errors or unexpected conditions 
	(http://support.robotis.com/en/product/dynamixel/communication/dxl_packet.htm)
	"""
	if p[2] != id:
		print 'Bad packet read (Unexpected id)'
		return -1

	if p[3] + 4 != len(p):
		print 'Bad packet read (Incorrect length)'
		return -1

	if p[4] != 0x00:
		print 'Bad packet read (Error bits set: ', p[4], ' [decimal representation])'
		return -1
 
	if p[-1] != checksumPacket(p[:-1]):
		print 'Bad packet read (bad checksum)'
		return -1

	return 0

def p2str( p ):
	""" Convert packet to string """
	return array.array('B', p).tostring();

def str2p( s ):
	""" Convert string to packet """
	return [ord(char) for char in list(s)]

def sendPacket( ser, p ):
	""" Send packet over serial channel """
	if PRINT_PACKETS:
		print 'sent:	 ', p
	i = ser.write(p2str(p))
	if i == 0:
		print 'No bytes written in sendPacket'
	return

def receivePacket( ser, id ):
	""" Read a packet waiting in the buffer """
	strHead = ser.read(4) # read packet up to length byte
	pHead = str2p(strHead)
	strTail = ser.read(pHead[3]) # read remaining bytes
	p = str2p(strHead + strTail)
	if checkPacket(id, p) != 0:
		return None
	if PRINT_PACKETS:
		print 'received: ', p
	return p