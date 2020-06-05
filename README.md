# Introduction
This code is for the KC868-H32 Smart home controller and domoticz.
This code gets INPUT/OUTPUT status (On, Off) and sends the data through API to domoticz smart home system.
# Usage
Firstly launch the kc868-h32.py, it is the main code to get info from the kincony device.
Test_req.py file is created to send many requests at once.
Update_device.py file is used to update KC868-H32 Relay On/Off through socket.

To update the device through update.py, you should use these parameters which are below.
```
  python3 update_device.py IP(192.168.1.0) PORT(4196) RELAY_NUMBER(1,32) RELAY_STATUS(0,1)
```
# Compatibility for other devices
If you would like to use another device from the same series you should change some functions and variables and you should be good to go.
