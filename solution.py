#from socket import *
#import os
#import sys
#import struct
#import time
#import select
#import binascii
#
#ICMP_ECHO_REQUEST = 8
#packetssent=0
#packetsreceived=0
#rttmin=999
#rttmax=0
#pinged=0
#totalrtt=0
#
#def checksum(string):
#    # In this function we make the checksum of our packet
#    csum = 0
#    countTo = (len(string) // 2) * 2
#    count = 0
#
#    for count in range(0, countTo, 2):
#        thisVal = string[count + 1] * 256 + string[count]
#        csum = csum + thisVal
#        csum = csum & 0xffffffff
#
#    if countTo < len(string):
#        csum = csum + string[-1]
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
#            bytesInDouble = struct.calcsize("d")
#            print("Reply from " + str(destAddr) + ":" + " bytes=" + str(bytesInDouble) + " ")
#            return "Request timed out."
#
#        timeReceived = time.time()
#        recPacket, addr = mySocket.recvfrom(1024)
#        global packetsreceived
#        packetsreceived = packetsreceived + 1
#        icmpHeader = recPacket[20:28]
#
#        ttl = struct.unpack("d", recPacket[0:8])[0]
#
#        icmpType, code, Checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
#
#        if (packetID == ID) :
#            bytesInDouble = struct.calcsize("d")
#            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
#            print("Reply from " + str(destAddr) + ":" + " bytes=" + str(bytesInDouble) + " ")
#            return timeReceived - timeSent
#
#        timeLeft = timeLeft - howLongInSelect
#        if timeLeft <= 0:
#            return "Request timed out."
#
#
#def sendOnePing(mySocket, destAddr, ID):
#    myChecksum = 0
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
#    myID = os.getpid() & 0xFFFF  # Return the current process i
#    sendOnePing(mySocket, destAddr, myID)
#    global packetssent
#    packetssent = packetssent + 1
#    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
#
#    mySocket.close()
#    return delay
#
#def ping(host, timeout=1):
#    dest = gethostbyname(host)
#    global pinged
#    if (pinged == 0):
#        print("Pinging " + dest + " using Python:")
#        print("")
#        pinged = 1
#    #Send ping requests to a server separated by approximately one second
#    while 1:
#        delay = doOnePing(dest, timeout)
#        if (delay == "Request timed out."):
#            print(delay)
#            print(" ")
#        else:
#            delay = delay * 1000
#            print("rtt = " + str(delay) + " ms")
#            print(" ")
#        time.sleep(1)  # one second
#        global totalrtt
#        global rttmin
#        global rttmax
#        if (delay != "Request timed out."):
#            if (delay < rttmin):
#                rttmin = delay
#            if (delay > rttmin):
#                rttmax = delay
#            totalrtt = totalrtt + delay
#        return delay

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

#hosttoping = "google.co.il"
#print("Pinging: " + hosttoping + " with 8 bytes of data")
#for i in range(0, 10):
#    ping(hosttoping)
#
#print("Ping Statistics for " + gethostbyname("www.poly.edu"))
#print("")
#print("Packets: Sent = " + str(packetssent))
#print("Packets: Received = " + str(packetsreceived))
#print("Packets: lost =" + str(packetssent - packetsreceived))
#if ((packetssent - packetsreceived) >= 0):
#    print("Packets: lost% = " + str(((packetssent - packetsreceived) / packetssent) * 100))
#else:
#    print("Packets: lost% = " + str(0))
#
#print("Minimum RTT: " + str(rttmin) + " ms")
#print("Maximum RTT: " + str(rttmax) + " ms")
#print("Average RTT: " + str(totalrtt / packetsreceived) + " ms")
#ping("google.co.il")
#################################################

from socket import *
import os
import sys
import struct
import time
import select
import binascii
# Should use stdev

ICMP_ECHO_REQUEST = 8
packetssent=0
packetsreceived=0
rttmin=999
rttmax=0
pinged=0
totalrtt=0

def checksum(string):
   csum = 0
   countTo = (len(string) // 2) * 2
   count = 0

   while count < countTo:
       thisVal = (string[count + 1]) * 256 + (string[count])
       csum += thisVal
       csum &= 0xffffffff
       count += 2

   if countTo < len(string):
       csum += (string[len(string) - 1])
       csum &= 0xffffffff

   csum = (csum >> 16) + (csum & 0xffff)
   csum = csum + (csum >> 16)
   answer = ~csum
   answer = answer & 0xffff
   answer = answer >> 8 | (answer << 8 & 0xff00)
   return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
   timeLeft = timeout

   while 1:
       startedSelect = time.time()
       whatReady = select.select([mySocket], [], [], timeLeft)
       howLongInSelect = (time.time() - startedSelect)
       if whatReady[0] == []:  # Timeout
           return "Request timed out."

       timeReceived = time.time()
       recPacket, addr = mySocket.recvfrom(1024)
       global packetsreceived
       packetsreceived +=  1
       icmpHeader = recPacket[20:28]
       # Fill in start
       ttl = struct.unpack("d", recPacket[0:8])[0]
       type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
       # Fetch the ICMP header from the IP packet
       if (packetID == ID):
           bytesInDouble = struct.calcsize("d")
           timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
           print("Reply from " + str(destAddr) + ":" + " bytes=" + str(bytesInDouble) + " " + ":"  + "ttl= " + str(ttl) + " ")
           return timeReceived - timeSent
       # Fill in end
       timeLeft = timeLeft - howLongInSelect
       if timeLeft <= 0:
           return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
   # Header is type (8), code (8), checksum (16), id (16), sequence (16)

   myChecksum = 0
   # Make a dummy header with a 0 checksum
   # struct -- Interpret strings as packed binary data
   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   data = struct.pack("d", time.time())
   # Calculate the checksum on the data and the dummy header.
   myChecksum = checksum(header + data)

   # Get the right checksum, and put in the header

   if sys.platform == 'darwin':
       # Convert 16-bit integers from host to network  byte order
       myChecksum = htons(myChecksum) & 0xffff
   else:
       myChecksum = htons(myChecksum)


   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   packet = header + data

   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


   # Both LISTS and TUPLES consist of a number of objects
   # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
   icmp = getprotobyname("icmp")


   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
   mySocket = socket(AF_INET, SOCK_RAW, icmp)

   myID = os.getpid() & 0xFFFF  # Return the current process i
   sendOnePing(mySocket, destAddr, myID)
   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
   mySocket.close()
   return delay


def ping(host, timeout=1):
   # timeout=1 means: If one second goes by without a reply from the server,      # the client assumes that either the client's ping or the server's pong is lost
   dest = gethostbyname(host)
   print("Pinging " + dest + " using Python:")
   print("")
   # Calculate vars values and return them
   #  vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
   # Send ping requests to a server separated by approximately one second
   for i in range(0,4):
       delay = doOnePing(dest, timeout)
       print(delay)
       time.sleep(1)  # one second

   return vars

if __name__ == '__main__':
   ping("google.co.il")







#################################################
#TraceROUTE LAB
#from socket import *
#import os
#import sys
#import struct
#import time
#import select
#import binascii
#
#ICMP_ECHO_REQUEST = 8
#MAX_HOPS = 30
#TIMEOUT = 2.0
#TRIES = 2
#
#
## The packet that we shall send to each router along the path is the ICMP echo
## request packet, which is exactly what we had used in the ICMP ping exercise.
## We shall use the same packet that we built in the Ping exercise
#def checksum(str):
#    # In this function we make the checksum of our packet
#    # hint: see icmpPing lab
#    csum = 0
#    countTo = (len(str) // 2) * 2
#    count = 0
#    while count < countTo:
#        thisVal = str[count + 1] * 256 + str[count]
#        csum = csum + thisVal
#        csum = csum & 0xffffffff
#        count = count + 2
#
#    if countTo < len(str):
#        csum = csum + str[len(str) - 1]
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
#def build_packet():
#    # In the sendOnePing() method of the ICMP Ping exercise, firstly the header of our
#    # packet to be sent was made, secondly the checksum was appended to the header and
#    # then finally the complete packet was sent to the destination.
#    # Make the header in a similar way to the ping exercise.
#    # Append checksum to the header.
#    # Don't send the packet yet , just return the final packet in this function.
#    # So the function ending should look like this packet = header + data return packet
#
#    ID = os.getpid() & 0xFFFF  # Return the current process i
#    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#    myChecksum = 0
#    # Make a dummy header with a 0 checksum.
#    # struct -- Interpret strings as packed binary data
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    data = struct.pack("d", time.time())
#    # Calculate the checksum on the data and the dummy header.
#    myChecksum = checksum(header + data)
#    # Get the right checksum, and put in the header
#    if sys.platform == 'darwin':
#        myChecksum = htons(myChecksum) & 0xffff
#        # Convert 16-bit integers from host to network byte order.
#    else:
#        myChecksum = htons(myChecksum)
#
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    packet = header + data
#
#    return packet
#
#
#def get_route(hostname):
#    # timeLeft = TIMEOUT     # Is this line in the wrong place? I changed it to three lines below......
#    print("Begin traceroute to " + hostname + "(" + gethostbyname(hostname) + ")......\n")
#
#    for ttl in range(1, MAX_HOPS):
#        for tries in range(TRIES):
#            timeLeft = TIMEOUT
#            destAddr = gethostbyname(hostname)
#            # Fill in start
#            # Make a raw socket named mySocket
#            icmp = getprotobyname("icmp")
#            try:
#                mySocket = socket(AF_INET, SOCK_RAW, icmp)
#            except error as msg:
#                print("Socket create error:", msg)
#            # Fill in end
#            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
#            mySocket.settimeout(TIMEOUT)
#            try:
#                d = build_packet()
#                mySocket.sendto(d, (hostname, 0))
#                t = time.time()
#                startedSelect = time.time()
#                whatReady = select.select([mySocket], [], [], timeLeft)
#                howLongInSelect = (time.time() - startedSelect)
#                if whatReady[0] == []:  # Timeout
#                    print("\t*\t\t*\t\t*\t\tRequest timed out.")
#                recvPacket, addr = mySocket.recvfrom(1024)
#                timeReceived = time.time()
#
#                timeLeft = timeLeft - howLongInSelect
#                if timeLeft <= 0:
#                    print("\t*\t*\t*\Request timed out.")
#            except timeout:
#                continue
#            else:
#                # Fill in start
#                # Fetch the icmp type from the IP packet
#
#                # get TTL
#                ttl = recvPacket[8]
#                # get ICMP info
#                type, pongCode, pongChecksum, pongID, pongSequence = struct.unpack("bbHHh", recvPacket[20:28])
#                # get RTT in ms
#                RTT = (timeReceived - struct.unpack("d", recvPacket[28:36])[0]) * 1000
#
#                # try to get hostname of each router in the path
#                try:
#                    routerHostname = gethostbyaddr(addr[0])[0]
#                except herror as emsg:
#                    routerHostname = "(Could not look up name:" + str(emsg) + ")"
#
#                # Fill in end
#                if type == 11:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
#                    print("TTL = %d\trtt=%.0f ms\tIP = %s\tHost:%s" % (
#                    ttl, (timeReceived - t) * 1000, addr[0], routerHostname))
#                elif type == 3:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
#                    print("TTL = %d\trtt=%.0f ms\tIP = %s\tHost:%s" % (
#                    ttl, (timeReceived - t) * 1000, addr[0], routerHostname))
#                elif type == 0:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
#                    print("TTL = %d\trtt=%.0f ms\tIP = %s\tHost:%s" % (
#                    ttl, (timeReceived - timeSent) * 1000, addr[0], routerHostname))
#                    return
#                else:
#                    print("error")
#                break
#            finally:
#                mySocket.close()
#
#
## traceroute four different host
#get_route("www.baidu.com")
#print("Traceroute Finished!\n\n\n\n\n\n")
#get_route("www.google.com")
#print("Traceroute Finished!\n\n\n\n\n\n")
#get_route("www.tsinghua.edu.cn")
#print("Traceroute Finished!\n\n\n\n\n\n")
#get_route("www.github.com")
#print("Traceroute Finished!\n\n\n\n\n\n")