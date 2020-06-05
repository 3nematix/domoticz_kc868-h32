# TCP connection - Send socket commands to device and set the relay to On/Off.
import socket
import sys

allowed_status = ['0', '1']

try:

    edsIP = str(sys.argv[1])
    edsPORT = int(sys.argv[2])
    relay_id = str(sys.argv[3])
    relay_status = str(sys.argv[4])

    STATE_INPUT = f'RELAY-SET-255,{relay_id},{relay_status}'

except IndexError:
    print('No arguments provided...')
    sys.exit()

# We only allow relay_status to be - 1,0.
if not relay_status in allowed_status:
    print('Relay status should be - (0,1).')
    sys.exit()

# Make a connection between server and kc868-h32.
try:

    srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srvsock.settimeout(3)
    srvsock.connect((edsIP, edsPORT))
    srvsock.sendto(STATE_INPUT.encode(), (edsIP, edsPORT))
    srvsock.close()

except Exception as er:
    print(er)
    sys.exit()

print('done...')
