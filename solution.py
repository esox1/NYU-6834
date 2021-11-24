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
#timeRTT = []
#packageSent =0;
#packageRev = 0;
#
#def checksum(string):
#   csum = 0
#   countTo = (len(string) / 2) * 2
#   count = 0
#
#   while count < countTo:
#       thisVal = (string[count + 1]) * 256 + (string[count])
#       csum = csum + thisVal
#       csum = csum & 0xffffffff
#       count = count + 2
#
#   if countTo < len(string):
#       csum = csum + (string[len(string) - 1])
#       csum = csum & 0xffffffff
#
#
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
#   global packageRev, timeRTT
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
#       icmpHeader = recPacket[20:28]
#       requestType, code, revChecksum, revID, revSequence = struct.unpack("bbHHh", icmpHeader)
#               # verify the ID of packet
#       if revID == ID:
#           bytesInDouble = struct.calcsize("d")
#           timeData = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
#           timeRTT.append(timeReceived - timeData)
#           packageRev += 1
#           return timeReceived - timeData
#
#       # Fill in end
#       timeLeft = timeLeft - howLongInSelect
#       if timeLeft <= 0:
#           return "Request timed out."
#
#
#def sendOnePing(mySocket, destAddr, ID):
#   # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#   global packageSent
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
#   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
#
#
#   # Both LISTS and TUPLES consist of a number of objects
#   # which can be referenced by their position number within the object.
#
#def doOnePing(destAddr, timeout):
#   icmp = getprotobyname("icmp")
#   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
#
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
#   # Send ping requests to a server separated by approximately one second
#   for i in range(0,4):
#       delay = doOnePing(dest, timeout)
#       print("RTT:", delay)
#       print( "maxRTT:", (max(timeRTT) if len(timeRTT) > 0 else 0), "\tminRTT:", (
#           min(timeRTT) if len(timeRTT) > 0 else 0), "\naverageRTT:", float(
#           sum(timeRTT) / len(timeRTT) if len(timeRTT) > 0 else float("nan")))
##       print( "Package Lose Rate:", ((packageSent - packageRev) / packageSent) if packageRev > 0 else 0)
#       time.sleep(1)  # one second
#   return delay
#
#
# #   vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
#
# #  return vars
#
##  for count in range(0, countTo, 2):
##      thisVal = (string[count + 1]) * 256 + (string[count])
##      csum = csum + thisVal
##      csum = csum & 0xffffffff
#
##  if countTo < len(string):
##      csum = csum + string[-1]
##      csum = csum & 0xffffffff
#
##if __name__ == '__main__':
#ping("google.co.il")
#

###################################################
#from socket import *
#import os
#import sys
#import struct
#import time
#import select
#import binascii
#
#ICMP_ECHO_REQUEST = 8
#
#
#def checksum(str_):
#    # In this function we make the checksum of our packet
#    str_ = bytearray(str_)
#    csum = 0
#    countTo = (len(str_) // 2) * 2
#
#    for count in range(0, countTo, 2):
#        thisVal = str_[count + 1] * 256 + str_[count]
#        csum = csum + thisVal
#        csum = csum & 0xffffffff
#
#    if countTo < len(str_):
#        csum = csum + str_[-1]
#        csum = csum & 0xffffffff
#
#    csum = (csum >> 16) + (csum & 0xffff)
#    csum = csum + (csum >> 16)
#    answer = ~csum
#    answer = answer & 0xffff
#    answer = answer >> 8 | (answer << 8 & 0xff00)
#    return answer
#
#
#def receiveOnePing(mySocket, ID, timeout, destAddr):
#    timeLeft = timeout
#    while 1:
#        startedSelect = time.time()
#        whatReady = select.select([mySocket], [], [], timeLeft)
#        howLongInSelect = (time.time() - startedSelect)
#        if whatReady[0] == []:  # Timeout
#            return "Request timed out."
#
#        timeReceived = time.time()
#        recPacket, addr = mySocket.recvfrom(1024)
#
#        icmpHeader = recPacket[20:28]
#        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
#
#        if type != 8 and packetID == ID:
#            bytesInDouble = struct.calcsize("d")
#            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
#            return timeReceived - timeSent
#
#        timeLeft = timeLeft - howLongInSelect
#
#        if timeLeft <= 0:
#            return "Request timed out."
#
#
#def sendOnePing(mySocket, destAddr, ID):
#    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#
#    myChecksum = 0
#    # Make a dummy header with a 0 checksum.
#    # struct -- Interpret strings as packed binary data
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    data = struct.pack("d", time.time())
#    # Calculate the checksum on the data and the dummy header.
#    myChecksum = checksum(header + data)
#
#    # Get the right checksum, and put in the header
#    if sys.platform == 'darwin':
#        myChecksum = htons(myChecksum) & 0xffff
#    # Convert 16-bit integers from host to network byte order.
#    else:
#        myChecksum = htons(myChecksum)
#
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    packet = header + data
#    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
#    # Both LISTS and TUPLES consist of a number of objects
#    # which can be referenced by their position number within the object
#
#
#def doOnePing(destAddr, timeout):
#    icmp = getprotobyname("icmp")
#    # Create Socket here
#    mySocket = socket(AF_INET, SOCK_DGRAM, icmp)
#
#    myID = os.getpid() & 0xFFFF  # Return the current process i
#    sendOnePing(mySocket, destAddr, myID)
#    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
#
#    mySocket.close()
#    return delay
#
#
#def ping(host, timeout=1):
#    dest = gethostbyname(host)
#    print("Pinging " + dest + " using Python:")
#    print("")
#    # Send ping requests to a server separated by approximately one second
#    while 1:
#        delay = doOnePing(dest, timeout)
#        print(delay)
#        time.sleep(1)  # one second
#    return delay
#
#
#ping("127.0.0.1")
#################################################


from socket import *
import socket
import os
import sys
import struct
import time
import select
import binascii

# use mac or linux terminal to run code using sudo Python testing.py
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(str_):
    # In this function we make the checksum of our packet
    str_ = bytearray(str_)
    csum = 0
    countTo = (len(str_) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = str_[count + 1] * 256 + str_[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(str_):
        csum = csum + str_[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet():
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    myChecksum = 0
    myID = os.getpid() & 0xFFFF

    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    # header = struct.pack("!HHHHH", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    # Append checksum to the header.
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet


def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = socket.gethostbyname(hostname)

            # Fill in start
            # Make a raw socket named mySocket
            icmp = socket.getprotobyname("icmp")
            # mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, icmp)
            # Fill in end

            mySocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)

                if whatReady[0] == []:  # Timeout
                    print("*    *    * Request timed out.")

                recvPacket, addr = mySocket.recvfrom(1024)
                print(addr)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    print("*    *    * Request timed out.")

            except socket.timeout:
                continue

            else:
                icmpHeader = recvPacket[20:28]
                request_type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

                if request_type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d   rtt=%.0f ms %s" % (ttl, (timeReceived - t) * 1000, addr[0]))
                elif request_type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d   rtt=%.0f ms %s" % (ttl, (timeReceived - t) * 1000, addr[0]))
                elif request_type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(" %d   rtt=%.0f ms %s" % (ttl, (timeReceived - timeSent) * 1000, addr[0]))
                    return
                else:
                    print("error")
                    break
            finally:
                mySocket.close()


'''
print("--------------------------------------------")                
print ('www.google.com')
print("--------------------------------------------")
get_route("www.google.com") # USA - North America
print("--------------------------------------------")
print ('www.china.org.cn')
print("--------------------------------------------")
get_route('www.china.org.cn') # China - Asia
print("--------------------------------------------")
print ('www.sweden.se')
print("--------------------------------------------")
get_route('www.sweden.se') # Sweden - Europe
print("--------------------------------------------")
print ('www.mybroadband.co.za')
print("--------------------------------------------")
get_route('www.mybroadband.co.za') # some place in Africa
'''

get_route('google.com')