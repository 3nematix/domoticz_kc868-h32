"""
    This code is to calculate input statuses for KC868-H32 Device.
    Made by: 3nematix (github)
"""

from test_req import Domoticz_req
import os
import pprint
import socket
import time

os.system('clear') # for mac os, if you using windows change it to - cls

edsIP = "192.168.11.4"  # IP address of your KC868-H32 device.
edsPORT = 4196  # PORT of your device.

domoticzIP = '192.168.1.124'
domoticzPORT = 8080
domoticzURL = 'http://' + domoticzIP + ':' + str(domoticzPORT) + '/json.htm'

STATE_INPUT = "RELAY-GET_INPUT-255"

current_ses = 0  # Create a little tracking system.

limited_calculations = False  # You can set a rate limitation for calculations.
limited_rate = 10  # If limited_calculations is set to True, you need to set a value.

# domoticz API Urls list.
urls = []

while True:
    try:
        calc_completed = False
        urls = []  # Overwrite

        current_ses += 1
        os.system('clear')

        # Limited rate of calculations available.
        if limited_calculations is True:
            if current_ses > limited_rate:
                print('Calculations have been completed, stopping the client.')
                break

        # Connect to the device using socket.

        srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srvsock.settimeout(3)
        srvsock.connect((edsIP, edsPORT))
        srvsock.sendto(STATE_INPUT.encode(), (edsIP, edsPORT))
        data = srvsock.recv(4096).decode('utf-8')
        if 'RELAY-ALARM' in data:
            time.sleep(2)
            continue

        # Replace the tags that we don't need for our further actions.
        try:
            data1 = data.replace('RELAY-GET_INPUT-255,', '')
            data2 = data1.replace(',OK', '')
            decimal_num = data2.rstrip('\x00')
        except Exception as er:
            print('Error,', er)
            time.sleep(2)

        # Convert a decimal number into a binary.
        binary = bin(int(decimal_num))[4:]  # We have 6 inputs in our device, so we need only 6 digits of binary.

        # Input status: 1 - OFF, 0 - ON. ( Binary )

        print(f'Session {current_ses} details:\nDecimal num received - {decimal_num}\nBinary converted - {binary}')

        # Sets INPUT status to default (False)
        Input1 = False
        Input2 = False
        Input3 = False
        Input4 = False
        Input5 = False
        Input6 = False

        # Always update the status of inputs, I'm trying to keep every status in real-time.
        # ( I will not use for loop , I want to do each one myself for better control in the future )

        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=Off') if \
            binary[5] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=On')
        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=off') if \
            binary[4] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=On')
        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=Off') if \
            binary[3] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=On')
        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=Off') if \
            binary[2] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=On')
        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=Off') if \
            binary[1] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=On')
        urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=Off') if \
            binary[0] == '1' else urls.append(
            'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=On')

        response = Domoticz_req.send_requests(urls)
        urls = []  # Empty the list.

        # Update 32 Relays statuses by real-time, in domoticz.
        for relay in range(1, 33):
            while True:

                if relay == 16:
                    urls_list = []

                    srvsock.sendto(STATE_INPUT.encode(), (edsIP, edsPORT))
                    data = srvsock.recv(4096).decode('utf-8')

                    if 'RELAY-ALARM' in data:
                        time.sleep(2)
                        continue

                    data1 = data.replace('RELAY-GET_INPUT-255,', '')
                    data2 = data1.replace(',OK', '')
                    decimal_num = data2.rstrip('\x00')

                    binary = bin(int(decimal_num))[4:]

                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=Off') if \
                        binary[5] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=On')
                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=off') if \
                        binary[4] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=On')
                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=Off') if \
                        binary[3] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=On')
                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=Off') if \
                        binary[2] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=On')
                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=Off') if \
                        binary[1] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=On')
                    urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=Off') if \
                        binary[0] == '1' else urls_list.append(
                        'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=On')

                    response = Domoticz_req.send_requests(urls_list)
                    urls_list = []


                RELAY_INPUT = f"RELAY-READ-255,{relay}"
                srvsock.sendto(RELAY_INPUT.encode(), (edsIP, edsPORT))

                _relay_status_ = srvsock.recv(4096).decode('utf-8').replace(f'RELAY-READ-255,{relay},', '').replace(',OK', '')
                _relay_status2_ = _relay_status_.rstrip('\x00')
                print(relay, 'Relay status is', _relay_status_)

                if 'RELAY-SET' in _relay_status_ or 'RELAY-ALARM' in _relay_status_:
                    _relay_status_ = srvsock.recv(4096).decode('utf-8').replace(f'RELAY-READ-255,{relay},', '').replace(',OK', '')
                    time.sleep(0.6)
                    continue

                _relay_status2_ = 'On' if _relay_status2_ == '1' else 'Off'
                urls.append(f'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx={relay}&switchcmd={_relay_status2_}')
                break

        # Once again we gonna update the inputs.
        while True:
            urls_list = []

            srvsock.sendto(STATE_INPUT.encode(), (edsIP, edsPORT))
            data = srvsock.recv(4096).decode('utf-8')

            if 'RELAY-ALARM' in data:
                time.sleep(2)
                continue

            data1 = data.replace('RELAY-GET_INPUT-255,', '')
            data2 = data1.replace(',OK', '')
            decimal_num = data2.rstrip('\x00')

            binary = bin(int(decimal_num))[4:]

            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=Off') if \
            binary[5] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=33&switchcmd=On')
            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=off') if \
            binary[4] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=34&switchcmd=On')
            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=Off') if \
            binary[3] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=35&switchcmd=On')
            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=Off') if \
            binary[2] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=36&switchcmd=On')
            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=Off') if \
            binary[1] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=37&switchcmd=On')
            urls_list.append('http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=Off') if \
            binary[0] == '1' else urls_list.append(
                'http://192.168.1.124:8080/json.htm?type=command&param=switchlight&idx=38&switchcmd=On')

            response = Domoticz_req.send_requests(urls_list)
            urls_list = []

            break

        calc_completed = True

    except Exception as er:
        print('Error', er)
        continue

    finally:
        # * Send our statistics to domoticz server.
        if calc_completed is True:
            if len(urls) < 32:
                print(len(urls))
                pprint.pprint(urls)
                print('Critical error - Not enough values... retrying...')
                srvsock.close()  # Stop the Client.
                time.sleep(5)  # Delay after re-starting calculations.
            else:
                response = Domoticz_req.send_requests(urls)
                print('*Sent to domoticz') if response is None else print('*Error sending info to domoticz.')
                srvsock.close()
                time.sleep(2)
        else:
            print('Critical error')
            srvsock.close()
            time.sleep(5)
