#BLE class
#esp_ble.py

from machine import Pin
from machine import Timer
import ubluetooth

import esp_context
import esp_parse_update

message = ""

class ESP32_BLE:
    def __init__(self, name):
        # Create internal objects for the onboard LED
        # blinking when no BLE device is connected
        # stable ON when connected
        self.led = Pin(2, Pin.OUT)
        self.timer0 = Timer(0)
        
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
#         print("MTU = ",self.ble.config('mtu'))

        
    def connected(self):
        self.led.value(1) 
        self.timer0.deinit()

    def disconnected(self):        
        self.timer0.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global message
        
        if event == 1: #_IRQ_CENTRAL_CONNECT:
                       # A central has connected to this peripheral
            self.connected()
            print("[esp32_BLE.py] BLE RC connected")

        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
                         # A central has disconnected from this peripheral.
            self.advertiser()
            self.disconnected()
            print("[esp32_BLE.py] BLE RC disconnected")
            esp_context.RC_data["gait"] = "STOP" #!!!! mind changing that to a particular behavior @ disconnect by introducing gait_disconnect
        
        elif event == 3: #_IRQ_GATTS_WRITE:
                         # A client has written to this characteristic or descriptor.          
            
            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            
           
            print("[esp32_BLE.py] ", message)
            
            
            ###PARSING###
#             rc_data_msg = message.split(":")
#             esp_context.RC_data[rc_data_msg[0]] = rc_data_msg[1]
            esp_parse_update.parse_and_update(message)
                
                               
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        # Convert name to bytes using UTF-8 encoding
        name_bytes = self.name.encode('utf-8')

        # Create the advertisement data
        adv_data = bytearray(b'\x02\x01\x02')  # Flags
        adv_data += bytearray([len(name_bytes) + 1, 0x09])  # Length and type for complete local name
        adv_data += name_bytes  # Name bytes

        # Start advertising
        self.ble.gap_advertise(100, adv_data)  
        


        print('[esp_ble.py] BLE advertising started:  ',self.name)
        print("\r\n")
                # adv_data
                # raw: 0x02010209094553503332424C45
                # b'\x02\x01\x02\t\tESP32BLE'
                #
                # 0x02 - General discoverable mode
                # 0x01 - AD Type = 0x01
                # 0x02 - value = 0x02
                
                # https://jimmywongiot.com/2019/08/13/advertising-payload-format-on-ble/
                # https://docs.silabs.com/bluetooth/latest/general/adv-and-scanning/bluetooth-adv-data-basics



led = Pin(2, Pin.OUT)

