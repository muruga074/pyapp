from pymodbus.client.sync_diag import ModbusTcpClient
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from datetime import datetime, time
import json
import random
import time

#CONNECTION_STRING = "HostName=PyIoTHub.azure-devices.net;DeviceId=My-IoT-Gateway;SharedAccessKey=OZxyvpQfLTUFQZ948U+XK1M5MrgbXId6abNy8yNcepI="
CONNECTION_STRING ="HostName=phc-pcm01-prd-iothub.azure-devices.net;DeviceId=7PGDMARZ;SharedAccessKey=nlB4sSkH6RUVmBUl4ZTVeEyzqnarM/WA03PeMMr16hk="

#MSG_TXT= '{{"data":{data}}}'
INTERVAL = 10
def current_time():
      now=datetime.now().isoformat()
      return now

#host = input('Enter the ip address of the device \n')
#port = input("Enter the port number \n")
host = ("192.168.1.4")
port = ('502')
modclient =ModbusTcpClient(host,port)  # type: ignore

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client =iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            modclient.connect()
            rr = modclient.read_holding_registers(1000,15,unit=1)
            #values =rr.registers
            val1=rr.registers[0]
            val2=rr.registers[1]
            val3=rr.registers[2]
            val4=(-1*rr.registers[3]/5)
            val5=(rr.registers[4]*random.randint(5,25))
            val6=rr.registers[5]
            val7=(round((rr.registers[6]/random.randint(10,50)),4))
            val8=rr.registers[7]
            val9=rr.registers[8]
            val10=rr.registers[9]
            val11=(round((30.98-float(rr.registers[10])),4))
            values1 = {"001": val1,"002": val2,"003": val3,"004": val4,"005": val5,"006": val6,"007": val7,"008": val8,"009": val9,"010": val10,"011": val11,}


            val =random.randint(0,9)
            print(val)
            if val == 0:
                def fun0():
                    return values1
                fun0()
                dbdefault=fun0()
                print('data0 : ',dbdefault)
                #break
            elif val %2 ==0 :
                def fun1(): 
                    return{
                    "001":val1,
                    "010":val10,
                    "005":val5}
            
                fun1()
                dbdefault=fun1()
                print('data1 :',dbdefault)
            else:
                def rdata():
                    return{
                        "006": val6,
                        "007": val7,
                        "008": val8,
                        "009": val9,
                        "010": val10,
                        "011": val11}
                rdata()
                dbdefault=rdata()
                print('data2 :',dbdefault)  
            
          
            print(values1)

            data={
                    'deviceId':"7PGDMARZ",
                    'productFilter': "pcmExternal",
                    "serial": "TEST-002",
                    'ts': current_time(),
                    "data_in":dbdefault               
            }
            #print(json.dumps(data))
            MSG_TXT = json.dumps(data) 
            message = Message(MSG_TXT)
            print("Sending message: ",json.dumps(data))
            client.send_message(message)
            print("Message sent")
            time.sleep(INTERVAL)  # type: ignore
    except KeyboardInterrupt:
        print("IotHubClient sample stopped")

if __name__ == '__main__':
    print("IoT Hub Quickstart - Reading from Modbus and sending to Azure")
    print("Press Ctrl-C to Exit")
    iothub_client_telemetry_sample_run()