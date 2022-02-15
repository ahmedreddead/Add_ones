import asyncore
import binascii
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import socket
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
ServerActive = False
Serverip = '185.222.242.249'
Serverport = 5029

broker_address = "192.168.0.100"
broker_address = "212.83.146.60"
broker_port = 5050
responsePacket = ''
def Save_IndexNum(index) :
    textfile = open("IndexNum.txt", "w")
    textfile.write(str (index))
    textfile.close()
def Load_IndexNum () :
    text_file = open("IndexNum.txt", "r")
    lines = text_file.readlines()
    Nlist = [i.replace("\n","").strip() for i in lines ]
    return Nlist[0]
def Set_IndexNumber () :
    Save_IndexNum(0)

def SendPacketHoldingDataBase(packet) :
    from influxdb import InfluxDBClient
    client = InfluxDBClient('192.168.0.100', 8086, 'home', 'home', 'Hold')
    try:
        index = Load_IndexNum()
    except :
        Set_IndexNumber()
        index =Load_IndexNum()

    DataPoint = [
        {
            "measurement": "Tzone",
            "fields": {
                "id": int (index) ,
                "Packet": packet
            }
        }
    ]
    index += 1
    Save_IndexNum(index)
    client.write_points(DataPoint)
def SendPacketToServer (packet) :
    if ServerActive:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((Serverip, Serverport))
            s.send(binascii.unhexlify(packet))
        except:
            print("server " + Serverip + "error")
def TestServerConnection () : #return network status
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((Serverip, Serverport))
        s.send(binascii.unhexlify("00"))
        return True
    except:
        return False
def mqttsend (jsonlist,sensoridlist) :
    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    print("connecting to broker")
    client.connect(broker_address ,broker_port)  # connect to broker
    #client.username_pw_set(username="homeassistant", password="yayeeheed8eezaechiwu4thahbaij2eiki0eim8Bo1chahbatief4Ohs1mait0Ph")
    #client.subscribe("LastAttendance")
    for i in range(len(jsonlist)):
        client.publish("Tzone/" + str(sensoridlist[i]), str(jsonlist[i]))
def Update_ACK (Packetindex) :
    global  responsePacket
    #str = '@CMD,*000000,@ACK,'+Packetindex+'#,#'
    str1 = '@ACK,'+Packetindex+'#'
    str1 = str1.encode('utf-8')
    responsePacket = str1.hex()
def ConvertRTCtoTime(RTC) :
    Year,Month,Day,Hours,Min,Sec = RTC[0:2],RTC[2:4],RTC[4:6],RTC[6:8],RTC[8:10],RTC[10:12]
    Year, Month, Day, Hours, Min, Sec =int(Year, 16),int(Month, 16),int(Day, 16),int(Hours, 16),int(Min, 16),int(Sec, 16)
    print("Date is ",Year,"/",Month,"/",Day)
    print("Time is ",Hours,"/",Min,"/",Sec)
    Date = str (Year)+"/"+str (Month) + "/"+str (Day)
    Time = str (Hours)+"/"+str (Min) + "/"+str (Sec)
    #return  Year, Month, Day, Hours, Min, Sec
    return  Date,Time
def TempFun ( temp) :
    sign = ''
    hexadecimal = temp
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    normalbit = padded_binary[0]
    postitive = padded_binary[1]
    value = padded_binary[2:]
    if str (normalbit) == '0' :
        pass
    else:
        return "Sensor error"

    if str (postitive) == '0':
        sign = '+'
    else:
        sign = '-'

    if sign == '+' :
        return str(int(value, 2)/10)

    else:
        return "-" + str(int(value, 2)/10)
def HumFun ( hum) :
    hexadecimal = hum
    end_length = len(hexadecimal) * 4
    hex_as_int = int(hexadecimal, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    normalbit = padded_binary[0]
    value = padded_binary[1:]
    if str (normalbit) == '0':
        pass
    else:
        return "Sensor error"
    return str(int(value, 2))
def ConvertPacketIntoElemets (packet) :
    if TestServerConnection() :
        SendPacketToServer(packet)
    else:
        SendPacketHoldingDataBase(packet)
    sensorfound = False
    NumberOfSensors = 0
    Sensorhexlist = []
    Packetindex = packet[-12:-8]
    print(Packetindex)
    Update_ACK(str ( int(Packetindex, 16)))
    Packetsensorlength = packet[76 :80]
    if int(Packetsensorlength, 16) != 0:
        sensorfound = True
        NumberOfSensors = packet[82:84]
        NumberOfSensors = int(NumberOfSensors, 16)
        print("Number Of Sensors", NumberOfSensors, "Sensor")
        result = 0
        for i in range(NumberOfSensors):
            i =i +result
            Sensorhexlist.append(packet[86+i:108+i])
            result+=21
    GatwayId = packet[24:40]
    print(GatwayId)
    RTC = packet[40:52]
    date,time = ConvertRTCtoTime(RTC)
    GatewayBattary = packet[68 :72 ]
    GatewayBattary = int(GatewayBattary, 16)/100
    print("Battary of Gateway ", GatewayBattary, "Volt")
    GatewayPower = packet[72 :76 ]
    GatewayPower = int(GatewayPower, 16)/100
    print("Power of Gateway ",GatewayPower, "Volt")
    print(sensorfound,NumberOfSensors,Sensorhexlist)
    ConvertSensorsToReadings(GatwayId,date,time,GatewayBattary,GatewayPower,NumberOfSensors,Sensorhexlist)
def ConvertSensorsToReadings (GatwayId,date,time,GatewayBattary,GatewayPower,NumberOfSensors,Sensorhexlist) :
    sensor_id_list = []
    sensor_temp_list = []
    sensor_hum_list = []
    sensor_battary_list = []
    jsonlist = []
    dectionarylist = []
    for packet in Sensorhexlist :
        sensor_id_list.append(packet[0:8])
        sensor_battary_list.append(int(packet[10:14], 16)/1000)
        sensor_temp_list.append(TempFun(packet[14:18]))
        sensor_hum_list.append(HumFun(packet[18:20]))
    print(sensor_id_list)
    print(sensor_temp_list)
    print(sensor_hum_list)
    print(sensor_battary_list)
    for index in range(NumberOfSensors) :
        jsonname = {"GatewayId": GatwayId,"GatewayBattary": GatewayBattary,"GatewayPower": GatewayPower , "Date": date, "Time": time ,
                "Sensorid": sensor_id_list[index] ,"SensorBattary": sensor_battary_list[index] ,"temperature" : sensor_temp_list[index] , "humidity": sensor_hum_list[index]
                    }
        dectionarylist.append(jsonname)
        print(json.dumps(jsonname))
        jsonlist.append(json.dumps(jsonname))
    #mqttsend(jsonlist,sensor_id_list)
    SendToInternalDataBase(dectionarylist)


def SendToInternalDataBaseToken (dectionarylist):
    bucket = "n"
    client = InfluxDBClient(url="http://localhost:8086",
                            token="n9cd2F9mYZcfhDE7892UzJv7xP38SSyQG9ybQRsYmGp6Bbv6OnbrGl5QGygzsZuzaCQTX-10w1EqY4axQNEzVg==",
                            org="skarpt")

    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    for i in dectionarylist :
        p = Point("Tzone").tag("gateway",i["Sensorid"]).field("temperature", float(i["temperature"])).time(datetime(2021, 12, 20, 0, 0), WritePrecision.US)
        write_api.write(bucket=bucket, record=p)
        print("database saved read")
def BuildJsonDataBase (Date, Time , Temp , Hum , Battery ,GateWayID, SensorID) :
    listofdate = Date.split("/")
    Year , Month , day = listofdate
    listoftime = Time.split("/")
    Hour , Mins , Sec = listoftime
    Year = "20" + Year
    ReadingTime = datetime(int (Year),int ( Month ) , int (day) , int (Hour) , int (Mins ),int (Sec)).isoformat() + "Z"
    JsonData = [
    {
        "measurement": "Tzone",
        "tags": {
            "SensorID": SensorID,
            "GatewayID" : GateWayID
        },
        "time": ReadingTime,
        "fields": {
            "Temperature": float(Temp),
            "Humidity": float(Hum),
            "Battery": float(Battery)
        }
    }
]
    return JsonData
def SendToInternalDataBase (dectionarylist):
    from influxdb import InfluxDBClient
    client = InfluxDBClient('192.168.0.100', 8086, 'home', 'home', 'example')
    for i in dectionarylist :
        DataPoint = BuildJsonDataBase(i["Date"],i["Time"],i["temperature"],i["humidity"],i["SensorBattary"],i["GatewayId"],i["Sensorid"])
        client.write_points(DataPoint)


Packetlist = []


class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        global  Packetlist
        data = self.recv(8192)
        if data:
            data = str ( binascii.hexlify(data).decode() )
            print(data)
            if data.startswith("545a") and  data.endswith("0d0a") and len(Packetlist) == 0 :
                ConvertPacketIntoElemets(data)
                self.send((binascii.unhexlify(responsePacket)))
            elif data.endswith("0d0a") :
                collectingpacket = ''
                for packetpart in Packetlist :
                    collectingpacket += packetpart
                collectingpacket += data
                ConvertPacketIntoElemets(collectingpacket)
                self.send((binascii.unhexlify(responsePacket)))
                Packetlist =[]
            else:
                Packetlist.append(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = EchoHandler(sock)


server = EchoServer('', 9090)
asyncore.loop()
