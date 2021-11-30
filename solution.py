#from socket import *
#import os
#import sys
#import struct
#import time
#import select
#import binascii
#import math
#
## Should use stdev
#
#ICMP_ECHO_REQUEST = 8
#
#
#def checksum(string):
#    csum = 0
#    countTo = (len(string) // 2) * 2
#    count = 0
#
#    while count < countTo:
#        thisVal = (string[count + 1]) * 256 + (string[count])
#        csum += thisVal
#        csum &= 0xffffffff
#        count += 2
#
#    if countTo < len(string):
#        csum += (string[len(string) - 1])
#        csum &= 0xffffffff
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
#
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
#        # Fill in start
#        header = recPacket[20:28]
#        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", header)
#
#        if type == 0 and packetID == ID:
#            bytesInDouble = struct.calcsize("d")
#            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
#            delay = timeReceived - timeSent
#            ttl = (struct.unpack("c", recPacket[8:9])[0].decode())
#            return (delay, ttl, bytesInDouble)
#
#        # Fill in end
#        timeLeft = timeLeft - howLongInSelect
#        if timeLeft <= 0:
#            return "Request timed out."
#
#
#def sendOnePing(mySocket, destAddr, ID):
#    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
#
#    myChecksum = 0
#    # Make a dummy header with a 0 checksum
#    # struct -- Interpret strings as packed binary data
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    data = struct.pack("d", time.time())
#    # Calculate the checksum on the data and the dummy header.
#    myChecksum = checksum(header + data)
#
#    # Get the right checksum, and put in the header
#
#    if sys.platform == 'darwin':
#        # Convert 16-bit integers from host to network  byte order
#        myChecksum = htons(myChecksum) & 0xffff
#    else:
#        myChecksum = htons(myChecksum)
#
#    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
#    packet = header + data
#
#    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
#
#    # Both LISTS and TUPLES consist of a number of objects
#    # which can be referenced by their position number within the object.
#
#
#def doOnePing(destAddr, timeout):
#    icmp = getprotobyname("icmp")
#
#    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
#    mySocket = socket(AF_INET, SOCK_RAW, icmp)
#
#    myID = os.getpid() & 0xFFFF  # Return the current process i
#    sendOnePing(mySocket, destAddr, myID)
#    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
#    mySocket.close()
#    return delay
#
#
#def ping(host, timeout=1):
#    # timeout=1 means: If one second goes by without a reply from the server,   # the client assumes that either the client's ping or the server's pong is lost
#    dest = gethostbyname(host)
#    # print("Pinging " + dest + " using Python:")
#    # print("")
#    # Calculate vars values and return them
#
#    lst = []
#    # Send ping requests to a server separated by approximately one second
#    for i in range(0, 4):
#        delay = doOnePing(dest, timeout)
#        # print(delay)
#        lst.append(round(delay[0] * 1000, 2))
#        time.sleep(1)  # one second
#
#    packet_min = min(lst)
#    packet_max = max(lst)
#    packet_avg = sum(lst) / len(lst)
#    stddev = 0
#    for i in lst:
#        stddev += (i - packet_avg) ** 2
#        #print(stddev)
#    stddev = math.sqrt((stddev / len(lst)))
#    # print(f'packet_min: {packet_min}, packet_max: {packet_max}, packet_avg: {packet_avg}, stddev: {stddev}')
#    vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)), str(round(stddev, 2))]
#    # print(vars)
#    return vars
#
#
#if __name__ == '__main__':
#    ping("google.co.il")

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
#MAX_HOPS = 30
#TIMEOUT = 2.0
#TRIES = 1
## The packet that we shall send to each router along the path is the ICMP echo
## request packet, which is exactly what we had used in the ICMP ping exercise.
## We shall use the same packet that we built in the Ping exercise
#
#def checksum(string):
## In this function we make the checksum of our packet
#    csum = 0
#    countTo = (len(string) // 2) * 2
#    count = 0
#
#    while count < countTo:
#        thisVal = (string[count + 1]) * 256 + (string[count])
#        csum += thisVal
#        csum &= 0xffffffff
#        count += 2
#
#    if countTo < len(string):
#        csum += (string[len(string) - 1])
#        csum &= 0xffffffff
#
#    csum = (csum >> 16) + (csum & 0xffff)
#    csum = csum + (csum >> 16)
#    answer = ~csum
#    answer = answer & 0xffff
#    answer = answer >> 8 | (answer << 8 & 0xff00)
#    return answer
#
#def build_packet():
#    #Fill in start
#    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
#    # packet to be sent was made, secondly the checksum was appended to the header and
#    # then finally the complete packet was sent to the destination.
#
#    # Make the header in a similar way to the ping exercise.
#    # Append checksum to the header.
#
#    # Don’t send the packet yet , just return the final packet in this function.
#    #Fill in end
#
#    # So the function ending should look like this
#
#        timeLeft = timeout
#
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
#        # Fill in start
#        header = recPacket[20:28]
#        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", header)
#
#        if type == 0 and packetID == ID:
#            bytesInDouble = struct.calcsize("d")
#            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
#            delay = timeReceived - timeSent
#            ttl = (struct.unpack("c", recPacket[8:9])[0].decode())
#            return (delay, ttl, bytesInDouble)
#
#        # Fill in end
#        timeLeft = timeLeft - howLongInSelect
#        if timeLeft <= 0:
#            return "Request timed out."
#    packet = header + data
#    return packet
#
#def get_route(hostname):
#    timeLeft = TIMEOUT
#    tracelist1 = [] #This is your list to use when iterating through each trace
#    tracelist2 = [] #This is your list to contain all traces
#
#    for ttl in range(1,MAX_HOPS):
#        for tries in range(TRIES):
#            destAddr = gethostbyname(hostname)
#
#            #Fill in start
#            # Make a raw socket named mySocket
#            #Fill in end
#
#            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
#            mySocket.settimeout(TIMEOUT)
#            try:
#                d = build_packet()
#                mySocket.sendto(d, (hostname, 0))
#                t= time.time()
#                startedSelect = time.time()
#                whatReady = select.select([mySocket], [], [], timeLeft)
#                howLongInSelect = (time.time() - startedSelect)
#                if whatReady[0] == []: # Timeout
#                    tracelist1.append("* * * Request timed out.")
#                    #Fill in start
#                    #You should add the list above to your all traces list
#                    #Fill in end
#                recvPacket, addr = mySocket.recvfrom(1024)
#                timeReceived = time.time()
#                timeLeft = timeLeft - howLongInSelect
#                if timeLeft <= 0:
#                    tracelist1.append("* * * Request timed out.")
#                    #Fill in start
#                    #You should add the list above to your all traces list
#                    #Fill in end
#            except timeout:
#                continue
#
#            else:
#                #Fill in start
#                #Fetch the icmp type from the IP packet
#                #Fill in end
#                try: #try to fetch the hostname
#                    #Fill in start
#                    #Fill in end
#                except herror:
#                    #if the host does not provide a hostname
#                    #Fill in start
#                    #Fill in end
#
#                if types == 11:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 +
#                    bytes])[0]
#                    #Fill in start
#                    #You should add your responses to your lists here
#                    #Fill in end
#                elif types == 3:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
#                    #Fill in start
#                    #You should add your responses to your lists here
#                    #Fill in end
#                elif types == 0:
#                    bytes = struct.calcsize("d")
#                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
#                    #Fill in start
#                    #You should add your responses to your lists here and return your list if your destination IP is met
#                    #Fill in end
#                else:
#                    #Fill in start
#                    #If there is an exception/error to your if statements, you should append that to your list here
#                    #Fill in end
#                break
#            finally:
#                mySocket.close()
#
#
#
#


#########################################################

from socket import *
import os
import sys
import struct
import time
import select
import binascii
ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise
def checksum(source_string):
    # In this function we make the checksum of our packet
    # hint: see icmpPing lab
    countTo = (int(len(source_string)/2))*2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (sys.byteorder == "little"):
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        try:     # For Python3
            sum = sum + (hiByte * 256 + loByte)
        except:  # For Python2
            sum = sum + (ord(hiByte) * 256 + ord(loByte))
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string): # Check for odd length
        loByte = source_string[len(source_string)-1]
        sum += loByte

    sum &= 0xffffffff # Truncate sum to 32 bits (a variance from ping.c, which
                      # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
    sum += (sum >> 16)                    # Add carry from above (if any)
    answer = ~sum & 0xffff                # Invert and truncate to 16 bits
    answer = htons(answer)

    return answer


def build_packet(time_str):
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    # Don’t send the packet yet , just return the final packet in this function.
    # So the function ending should look like this

    # Header is type (8), code (8),checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct --Interpret strings as packed binary data
    ID = os.getpid() & 0xFFFF
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time_str)
    '''
    padBytes = []
    startVal = 0x42
    for i in range(startVal, startVal + (64-8)):
        padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
    data = bytearray(padBytes)
    '''
    myChecksum = checksum(header + data) # Checksum is in network order

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "!BBHHH", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1
    )
    packet = header + data
    return packet


def get_route(hostname):
    destAddr = gethostbyname(hostname)
    timeLeft = TIMEOUT
    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):


            icmp = getprotobyname('icmp')
            # Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, icmp)

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                for i in range(3):
                    d = build_packet(time.time())
                    mySocket.sendto(d, (hostname, 0))

                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    print(" * * * Request timed out in select!")
                    continue

                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                recvPacket, addr = mySocket.recvfrom(1024)
                if recvPacket != None:
                    #print("addr: {}".format(addr))
                    destAddr = addr
                    header = recvPacket[20:28]
                    #print("header:{}".format(header))
                    # gets the type from the packet
                    types, code, checksum, ID, seq = struct.unpack("!BBHHH", header)
                    #print("got packet type: {}".format(types))
                    bytes = struct.calcsize("d")
                    if types == 11: # TTL excceed
                        timeSent = struct.unpack("d", recvPacket[28:36])[0]
                        #print("type 11")
                        print(" {} rtt={} ms {}".format(ttl, int((timeReceived - timeSent)*1000), addr[0]))
                    elif types == 3: # dest unreachable
                        #print("type 3")
                        timeSent = struct.unpack("d", recvPacket[28:36])[0]
                        print(" {} rtt={} ms {}".format(ttl, int((timeReceived - timeSent)*1000), addr[0]))
                    elif types == 0:
                        #print("type 0")
                        timeSent = struct.unpack("d", recvPacket[28:36])[0]
                        #print(timeSent)
                        rtt = int((timeReceived - timeSent)*1000)
                        print("rtt = {} ms {}".format(rtt, gethostbyaddr(destAddr[0])))
                        return
                    else:
                        print("error")
                        break
                #print("got packet:{}".format(recvPacket))
                if timeLeft <= 0:
                    print(" * * * Request timed out in time left!")
            except timeout:
                continue
            finally:
                    mySocket.close()
                    break

if __name__ == '__main__':
    get_route("google.com")