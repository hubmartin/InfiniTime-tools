# Infinitime BLE tools

Various scripts and tools for InfiniTime watch firmware

## BLE NUS serial terminal

You can use `ble-serial.py` for communicating with InfiniTime firmware with BLE NUS support https://github.com/JF002/InfiniTime/pull/560

This code can be used with any NRF NUS serial BLE UART.

Example:

```
➜  mqtt-ble-python ./discover.py 
DC:8F:0A:FE:3F:6E: InfiniTimeP8
00:81:F9:53:FE:01: SMILE
```

Copy BLE address and call

```
./ble-serial.py DC:8F:0A:FE:3F:6E
```

Now test command `AT`, or `WKUP`, `SLEEP`.

```
➜  mqtt-ble-python ./ble-serial.py DC:8F:0A:FE:3F:6E
Connected on DC:8F:0A:FE:3F:6E
AT
OK
WKUP
SLEEP
LVGL
used:   3912 ( 28 %), frag:   1 %, biggest free:  10368
children: 12
#0, x: 198, y: 217, w: 25, h: 23
#1, x: 228, y: 217, w: 12, h: 23
#2, x: 25, y: 217, w: 0, h: 23
```

Keywords:
- BLE
- NRF52832, NRF52840
