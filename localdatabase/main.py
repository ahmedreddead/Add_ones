import asyncore
import binascii
import json
import threading
from datetime import datetime
import paho.mqtt.client as mqtt
import socket
from datetime import date

from influxdb import InfluxDBClient
import PyCRC
from PyCRC.crc import CRC

#from influxdb_client import InfluxDBClient, Point, WritePrecision #Token
#from influxdb_client.client.write_api import SYNCHRONOUS #Token
full_packet_list = []
ServerActive = True
Serverip = '185.222.242.249'
Serverport = 5029
broker_address = "192.168.0.100"
broker_port = 1883
responsePacket = ''
response2 = ''
#INTERNAL_DATABASE_NAME = "example"
#INTERNAL_BACKUP_DATABASE_NAME = "Hold"
#USERNAME_DATABASE = "home"
#PASSWORD_DATABASE = "home"
#DATABASE_IP = '192.168.0.100'
#measurement = "Tzone"

DATABASE_PORT = '8086'
USERNAME_DATABASE = str(open("config/USERNAME_DATABASE.txt", "r").read()).strip()
PASSWORD_DATABASE = str(open("config/PASSWORD_DATABASE.txt", "r").read()).strip()
INTERNAL_BACKUP_DATABASE_NAME = str(open("config/INTERNAL_BACKUP_DATABASE_NAME.txt", "r").read()).strip()
INTERNAL_DATABASE_NAME = str(open("config/INTERNAL_DATABASE_NAME.txt", "r").read()).strip()
DATABASE_IP = str(open("config/DATABASE_IP.txt", "r").read()).strip()
measurement = str(open("config/measurement.txt", "r").read()).strip()


def ConvertKSA (packet) :
    hour = packet[46:48]
    print(int(hour, 16))
    newtime = str(hex(int(hour, 16) + 1)).replace("0x", "")
    if len(newtime) == 1:
        newtime = "0" + newtime
    newpacket = packet[:46] + newtime + packet[48:]
    return newpacket
def Checked_SavedHolding_Database():
    client = InfluxDBClient(DATABASE_IP, DATABASE_PORT, USERNAME_DATABASE, PASSWORD_DATABASE, INTERNAL_BACKUP_DATABASE_NAME)
    result = client.query('SELECT *  FROM '+str(INTERNAL_BACKUP_DATABASE_NAME)+'."autogen".'+str(measurement))
    length = len(list(result.get_points()))
    if length != 0 :
        return True
    else:
        return False
def Send_Saved_Database ():
    client = InfluxDBClient(DATABASE_IP, DATABASE_PORT, USERNAME_DATABASE, PASSWORD_DATABASE, INTERNAL_BACKUP_DATABASE_NAME)
    result = client.query('SELECT *  FROM '+str(INTERNAL_BACKUP_DATABASE_NAME)+'."autogen".'+str(measurement))
    data = list(result.get_points())
    for point in data :
        SendPacketToServer(str(point["Packet"]))
        client.delete_series(database=INTERNAL_BACKUP_DATABASE_NAME, measurement=measurement, tags={"id":point["id"]})
def Save_IndexNum(index) :
    textfile = open("IndexNum.txt", "w")
    textfile.write(str (index))
    textfile.close()
def Load_IndexNum () :
    text_file = open("IndexNum.txt", "r")
    lines = text_file.readlines()
    Nlist = [i.replace("\n","").strip() for i in lines ]
    return int (Nlist[0])
def Set_IndexNumber () :
    Save_IndexNum(0)
def SendPacketHoldingDataBase(packet) :
    from influxdb import InfluxDBClient
    client = InfluxDBClient(DATABASE_IP, DATABASE_PORT, USERNAME_DATABASE, PASSWORD_DATABASE, INTERNAL_BACKUP_DATABASE_NAME)
    try:
        index = Load_IndexNum()
    except :
        Set_IndexNumber()
        index =Load_IndexNum()

    DataPoint = [
        {
            "measurement": measurement,
            "tags" : {
                "id": index
            },
            "fields": {
                "Packet": packet
            }
        }
    ]
    index += 1
    Save_IndexNum(index)
    client.write_points(DataPoint)
def SendPacketToServer (packet) :
    packet = ConvertKSA(packet)
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
        client.publish(measurement+"/" + str(sensoridlist[i]), str(jsonlist[i]))
def Update_ACK (Packetindex) :
    global  responsePacket,response2
    #str = '@CMD,*000000,@ACK,'+Packetindex+'#,#'
    str1 = '@ACK,'+Packetindex+'#'
    str1 = str1.encode('utf-8')
    responsePacket = str1.hex()
    response2 = "Server UTC time:"+str(datetime.now())[:19]
    response2 = response2.encode('utf-8')
    response2 = response2.hex()
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

def logic(packet):
    if TestServerConnection() :
        SendPacketToServer(packet)
        if Checked_SavedHolding_Database() :
            threading.Thread(target=Send_Saved_Database, args=[]).start()
    else:
        SendPacketHoldingDataBase(packet)
        
def ConvertPacketIntoElemets (packet) :

    threading.Thread(target=logic, args=[packet]).start()
    
    sensorfound = False
    NumberOfSensors = 0
    Sensorhexlist = []
    Packetindex = packet[-12:-8]
    print(Packetindex)
    Update_ACK(str ( int(Packetindex, 16)))
    Packetsensorlength = packet[76:80]
    if Packetsensorlength == "0000":
        return 0
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
    del jsonname,jsonlist,sensor_id_list,sensor_temp_list,sensor_hum_list,sensor_battary_list,GatwayId,date,time,GatewayBattary,GatewayPower,NumberOfSensors,Sensorhexlist
    SendToInternalDataBase(dectionarylist)
'''
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
'''
def BuildJsonDataBase (Date, Time , Temp , Hum , Battery ,GateWayID, SensorID) :
    listofdate = Date.split("/")
    Year , Month , day = listofdate
    listoftime = Time.split("/")
    Hour , Mins , Sec = listoftime
    Year = "20" + Year
    ReadingTime = datetime(int (Year),int ( Month ) , int (day) , int (Hour) , int (Mins ),int (Sec)).isoformat() + "Z"
    JsonData = [
    {
        "measurement": measurement,
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
    client = InfluxDBClient(DATABASE_IP, DATABASE_PORT , USERNAME_DATABASE, PASSWORD_DATABASE, INTERNAL_DATABASE_NAME)
    for i in dectionarylist :
        DataPoint = BuildJsonDataBase(i["Date"],i["Time"],i["temperature"],i["humidity"],i["SensorBattary"],i["GatewayId"],i["Sensorid"])
        client.write_points(DataPoint)
    del  dectionarylist

def check_packet(data) :
    check_code = data[-8:- 4]
    # The range is from Protocol type to Packet index(include Protocol type and Packet index)
    hex_data = data[8:-8]
    our_model = PyCRC.CRC_16_MODBUS
    crc = CRC.CRC(hex_data, our_model)

    if check_code.lower() == crc.lower() :
        return True
    else:
        return False

def preprocess_packet(data):
    global full_packet_list

    data = str(binascii.hexlify(data).decode())
    print(data)
    data = data.strip()
    if data.startswith("545a") and data.endswith("0d0a"):
        full_packet_list = []
        if check_packet(data) :
            ConvertPacketIntoElemets(data)
        return [binascii.unhexlify(responsePacket.strip()) , binascii.unhexlify(response2.strip())]
    elif data.endswith("0d0a") and not data.startswith("545a") and full_packet_list :
        collecting_packet = ''
        for packet_part in full_packet_list:
            collecting_packet += packet_part
        collecting_packet += data
        if check_packet(collecting_packet):
            ConvertPacketIntoElemets(collecting_packet)
        full_packet_list = []
        return [binascii.unhexlify(responsePacket.strip()), binascii.unhexlify(response2.strip())]
    else:
        full_packet_list.append(data)

    return 0

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            try:
                send_list = preprocess_packet(data)
                if send_list != 0 :
                    for i in send_list :
                        self.send(i)
            except :
                pass


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


server = EchoServer('', 2000)
asyncore.loop()
