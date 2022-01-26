import asyncore
import binascii
import socket
import paho.mqtt.client as mqtt
import datetime
from datetime import date
broker_address = "192.168.0.100"
Temp , Hum , Battary, ID , WIFI ,Date , Time ='', '', '' , '', '', '',''
responsePacket = ''
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

    global Date,Time

    Date = str (Year)+"/"+str (Month) + "/"+str (Day)
    Time = str (Hours)+"/"+str (Min) + "/"+str (Sec)

    return  Year, Month, Day, Hours, Min, Sec
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


    return str(int(value, 2)/10)
def ConvertPacketIntoElemets (packet) :
    global ID,WIFI,Battary,Temp,Hum
    GatwayId = packet[24:40]
    ID = str(GatwayId)

    print('GatwayId is ',GatwayId)
    RTC = packet[40:52]
    ConvertRTCtoTime(RTC)

    Wifisignal = int(packet[60:62], 16)
    print('Wifi Signal is ', Wifisignal)
    WIFI =str (Wifisignal)

    battary = int(packet[64:68], 16)
    print('Battary is ', battary/100)
    Battary =str (battary/100)

    Temperature=TempFun (packet[68:72])
    print('Temperature is ', Temperature , "C")
    Temp = str(Temperature)

    Humidity = HumFun(packet[72:76] )
    print('Humidity is ', Humidity, "%")
    Hum = str(Humidity)

    Packetindex = int(packet[76:80], 16)

    print('Packet index is ', Packetindex)
    Update_ACK(str (Packetindex))
def mqtt_send ():
    print("creating new instance")
    client = mqtt.Client("P1")  # create new instance
    # client.tls_set()  # <--- even without arguments
    #client.username_pw_set(username="mqtt-user", password="0000")
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.publish("Tzone/"+ID+'/TEMP', Temp)
    client.publish("Tzone/"+ID+'/Hum', Hum)
    client.publish("Tzone/"+ID+'/Battary', Battary)
    client.publish("Tzone/"+ID+'/WIFI', WIFI)
    client.publish("Tzone/"+ID+'/Date', Date)
    client.publish("Tzone/"+ID+'/Time', Time)
    
def Get_Date():
    today = date.today()
    d3 = today.strftime("%m/%d/%y")
    d3 = d3.split('/')
    month = hex(int(d3[0])).replace("0x", "")
    day = hex(int(d3[1])).replace("0x", "")
    year = hex(int(d3[2])).replace("0x", "")
    if len(month) == 1:
        month = month.replace(month, "0" + month)
    if len(day) == 1:
        day = day.replace(day, "0" + day)
    if len(year) == 1:
        year = year.replace(year, "0" + year)
    a= month + day
    return a
def Get_Time() :
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    d3 = current_time.split(':')
    hour = hex(int(d3[0])).replace("0x", "")
    minits = hex(int(d3[1])).replace("0x", "")
    sec = hex(int(d3[2])).replace("0x", "")
    if len(hour) == 1:
        hour = hour.replace(hour, "0" + hour)
    if len(minits) == 1:
        minits = minits.replace(minits, "0" + minits)
    if len(sec) == 1:
        sec = sec.replace(sec, "0" + sec)
    a= hour + minits + sec
    return a
def chainees_sensor (packet) :
# Framehead 2 +length 2 + framenumber 1 + frametype 1 + (data) N+ checkout 1
# FBFB 000A 02 81 07E6 0911090D19 64
# FBFB 000D AE 01 00081EFAFCE0EBA53500  24
    global responsePacket
    framenumber = packet[8:10]
    responsePacket = "FBFB000A"+framenumber+"8107E6"+str(Get_Date())+str(Get_Time())+"64"
class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        Serverip = '192.168.0.121'
        Serverport = 8080
        if data:
            print(data)
            #ConvertPacketIntoElemets(binascii.hexlify(data).decode())
            chainees_sensor(binascii.hexlify(data).decode())
            print(responsePacket)
            self.send((binascii.unhexlify(responsePacket)))
            #mqtt_send()
            
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((Serverip, Serverport))
                s.send(binascii.hexlify(data))
                print("message sent")
            except:
                print("server " + Serverip + " error")
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


server = EchoServer('', 9060)
asyncore.loop()
