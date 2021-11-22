#!/usr/bin/python
# -*- coding: utf-8 -*-
from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8


def checksum(myString):

# In this function we make the checksum of our packet

    myString = bytearray(myString)
    csum = 0
    countTo = len(myString) // 2 * 2

    for count in range(0, countTo, 2):
        thisVal = myString[count + 1] * 256 + myString[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(myString):
        csum = csum + myString[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 65535)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 65535
    answer = answer >> 8 | answer << 8 & 0xff00
    return answer


def receiveOnePing(
    mySocket,
    ID,
    timeout,
    destAddr,
    ):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = time.time() - startedSelect
        if whatReady[0] == []:  # Timeout
            return 'Request timed out.'

        timeReceived = time.time()
        (recPacket, addr) = mySocket.recvfrom(1024)

# accessing icmp header from packet

        icmpHeader = recPacket[20:28]
        (icmpType, code, mychecksum, packetID, sequence) = \
            struct.unpack('bbHHh', icmpHeader)

# verify the ID of packet

        if icmpType != 8 and packetID == ID:
            bytesInDouble = struct.calcsize('d')
            timeSent = struct.unpack('d', recPacket[28:28
                    + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect

        if timeLeft <= 0:
            return 'Request timed out.'


def sendOnePing(mySocket, destAddr, ID):

# Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0

# Make a dummy header with a 0 checksum.
# struct -- Interpret strings as packed binary data

    header = struct.pack(
        'bbHHh',
        ICMP_ECHO_REQUEST,
        0,
        myChecksum,
        ID,
        1,
        )
    data = struct.pack('d', time.time())

# Calculate the checksum on the data and the dummy header.

    myChecksum = checksum(header + data)

# Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 65535
    else:

# Convert 16-bit integers from host to network byte order.

        myChecksum = htons(myChecksum)

    header = struct.pack(
        'bbHHh',
        ICMP_ECHO_REQUEST,
        0,
        myChecksum,
        ID,
        1,
        )
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


# Both LISTS and TUPLES consist of a number of objects
# which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = getprotobyname('icmp')

# Create Socket here

    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 65535  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    dest = gethostbyname(host)
    print 'Pinging ' + dest + ' using Python:'
    print ''

    loop = 0

# Send ping requests to a server separated by approximately one second

    while loop < 10:
        delay = doOnePing(dest, timeout)
        print delay
        time.sleep(1)  # sleep one second
        loop += 1  # for loop-limit
    return delay


# Picked IP of different continent from:
# https://www.dotcom-monitor.com/blog/technical-tools/network-location-ip-addresses/

print 'Ping to Washington DC'
ping('23.81.0.59')  # Washington DC

print '-----------------------'
print 'Ping to China'
ping('www.china.org.cn')  # china

print '-----------------------'
print 'Ping to Australia'
ping('223.252.19.130')  # Brisbane, Australia

print '-----------------------'
print 'Ping to Europe'
ping('95.142.107.181')  # Amsterdam




#from socket import *
#import os
#import sys
#import struct
#import time
#import select
#import binascii
## Should use stdev
#
#ICMP_ECHO_REQUEST = 8
#
#
#def checksum(string):
#   csum = 0
#   countTo = (len(string) // 2) * 2
#   count = 0
#
#   while count < countTo:
#       thisVal = (string[count + 1]) * 256 + (string[count])
#       csum += thisVal
#       csum &= 0xffffffff
#       count += 2
#
#   if countTo < len(string):
#       csum += (string[len(string) - 1])
#       csum &= 0xffffffff
#
#   csum = (csum >> 16) + (csum & 0xffff)
#   csum = csum + (csum >> 16)
#   answer = ~csum
#   answer = answer & 0xffff
#   answer = answer >> 8 | (answer << 8 & 0xff00)
#   return answer
#
#
#
#def receiveOnePing(mySocket, ID, timeout, destAddr):
#   timeLeft = timeout
#
#   while 1:
#       startedSelect = time.time()
#       whatReady = select.select([mySocket], [], [], timeLeft)
#       howLongInSelect = (time.time() - startedSelect)
#       if whatReady[0] == []:  # Timeout
#           return "Request timed out."
#
#       timeReceived = time.time()
#       recPacket, addr = mySocket.recvfrom(1024)
#
#       # Fill in start
#
#       # Fetch the ICMP header from the IP packet
#
#       # Fill in end
#       timeLeft = timeLeft - howLongInSelect
#       if timeLeft <= 0:
#           return "Request timed out."
#
#
#def sendOnePing(mySocket, destAddr, ID):
#   # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#
#   myChecksum = 0
#   # Make a dummy header with a 0 checksum
#   # struct -- Interpret strings as packed binary data
#   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#   data = struct.pack("d", time.time())
#   # Calculate the checksum on the data and the dummy header.
#   myChecksum = checksum(header + data)
#
#   # Get the right checksum, and put in the header
#
#   if sys.platform == 'darwin':
#       # Convert 16-bit integers from host to network  byte order
#       myChecksum = htons(myChecksum) & 0xffff
#   else:
#       myChecksum = htons(myChecksum)
#
#
#   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#   packet = header + data
#
#   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
#
#
#   # Both LISTS and TUPLES consist of a number of objects
#   # which can be referenced by their position number within the object.
#
#def doOnePing(destAddr, timeout):
#   icmp = getprotobyname("icmp")
#
#
#   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
#   mySocket = socket(AF_INET, SOCK_RAW, icmp)
#
#   myID = os.getpid() & 0xFFFF  # Return the current process i
#   sendOnePing(mySocket, destAddr, myID)
#   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
#   mySocket.close()
#   return delay
#
#
#def ping(host, timeout=1):
#   # timeout=1 means: If one second goes by without a reply from the server,      # the client assumes that either the client's ping or the server's pong is lost
#   dest = gethostbyname(host)
#   print("Pinging " + dest + " using Python:")
#   print("")
#   # Calculate vars values and return them
#   #  vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
#   # Send ping requests to a server separated by approximately one second
#   for i in range(0,4):
#       delay = doOnePing(dest, timeout)
#       print(delay)
#       time.sleep(1)  # one second
#
#   return vars
#
#if __name__ == '__main__':
#   ping("google.co.il")
