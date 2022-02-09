import asyncore
import binascii
import socket
import paho.mqtt.client as mqtt
from datetime import date
from datetime import datetime
import time

broker_address = "192.168.0.100"
Temp,Hum ,ID, Date = '', '', '', ''
responsePacket = ''
def get_bcc(inputStr):
    bcc = 0
    ar = []
    for i in range(0, len(inputStr), 2):
        ar.append(inputStr[i] + inputStr[i + 1])
    for i in ar:
        bcc = bcc ^ int(i, 16)
    return f'{bcc:x}'
def get_length (packet) :
    value = str (hex (len(packet)//2)).replace("0x","")
    if len(value) == 1 :
        return "000"+value
    elif len(value) == 2 :
        return "00" + value
    elif len(value) == 3 :
        return "0" + value
    else :
        return value
def convert_time (hextime) :
    Y = hextime[0:4]
    M = hextime[4:6]
    D = hextime[6:8]
    H = hextime[8:10]
    m = hextime[10:12]
    s = hextime[12:14]
    return str(int(Y, 16))+"/"+str(int(M, 16))+"/"+str(int(D, 16))+"  "+str(int(H, 16))+":"+str(int(m, 16))+":"+str(int(s, 16))
def convert_readings (readings,NumOfReadings) :
    n=0
    tempReadings = ""
    humReadings = ""
    for i in range(NumOfReadings) :
        read = readings[0+n:8+n]
        Temp = int(read[0:4],16)/10
        hum = int(read[4:8],16)
        if Temp > 1000 :
            Temp= str("-")+str(Temp)[2:]
        tempReadings +=str(Temp)+" ℃"+" "
        humReadings +=str(hum)+" %RH"+" "
        n+=8
    return tempReadings,humReadings
def mqtt_send():
    print("creating new instance")
    client = mqtt.Client("Freshliance")  # create new instance
    # client.tls_set()  # <--- even without arguments
    client.username_pw_set(username="homeassistant", password="yayeeheed8eezaechiwu4thahbaij2eiki0eim8Bo1chahbatief4Ohs1mait0Ph")
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.publish("Freshliance" + '/ID', ID)
    client.publish("Freshliance" + '/TEMP', Temp)
    client.publish("Freshliance" + '/Hum', Hum)
    client.publish("Freshliance" + '/Date', Date)
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
    a = month + day
    return a
def Get_Time():
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
    a = hour + minits + sec
    return a
def getinfo(packet,frameType):
    global ID,Date,Temp,Hum
    if str(frameType) == "01" :
        ID = packet[14:32]
    elif str(frameType) == "03" :
        hextime = packet[16:30]
        duration = packet[30:34]
        readings = packet[36:-2]
        NumOfRead = len(readings) // 8
        Temp, Hum = convert_readings(readings, NumOfRead)
        Date = convert_time(hextime)
        mqtt_send()
def chainees_sensor(packet):
    # Framehead 2 +length 2 + framenumber 1 + frametype 1 + (data) N+ checkout 1
    # FBFB 000A 02 81 07E6 0911090D19 64
    # FBFB 000D AE 01 00081EFAFCE0EBA53500  24
    global responsePacket
    framenumber = packet[8:10]
    frameType = packet[10:12]
    Time = "07E6" + str(Get_Date()) + str(Get_Time())
    if str(frameType) == "01" :
        Type = "81"
        checkout = str ( get_bcc(framenumber+Type+Time) )
        length = get_length(framenumber+Type+Time+checkout)
        if len(checkout) == 1 :
            checkout = "0"+checkout
        responsePacket = "FBFB"+length+ framenumber + Type + Time + checkout
        getinfo(packet,frameType)
    elif str(frameType) == "02" :
        Type = "82"
        checkout = str ( get_bcc(framenumber+Type+Time))
        if len(checkout) == 1 :
            checkout = "0"+checkout
        length = get_length(framenumber+Type+Time+checkout)
        responsePacket = "FBFB" + length + framenumber + Type + Time + checkout
    elif str(frameType) == "03" :
        Type = "83"
        checkout = str (get_bcc(framenumber+Type))
        if len(checkout) == 1 :
            checkout = "0"+checkout
        length = get_length(framenumber+Type+checkout)
        responsePacket = "FBFB"+length + framenumber + Type + checkout
        getinfo(packet,frameType)
    else:
        responsePacket = "0000"


class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        #Serverip = '192.168.0.121'
        #Serverport = 8080
        if data:
            print(data)
            print(binascii.hexlify(data).decode())
            chainees_sensor(binascii.hexlify(data).decode())
            print(responsePacket)
            self.send((binascii.unhexlify(responsePacket)))
            # mqtt_send()

        #    try:
        #        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #        s.connect((Serverip, Serverport))
        #        s.send(binascii.hexlify(data))
        #        print("message sent")
        #    except:
        #        print("server " + Serverip + " error")


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
