import asyncore
import binascii
import paho.mqtt.client as mqtt
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
    client.username_pw_set(username="mqtt-user", password="0000")
    print("connecting to broker")
    client.connect(broker_address)  # connect to broker
    client.publish("Tzone/"+ID+'/TEMP', Temp)
    client.publish("Tzone/"+ID+'/Hum', Hum)
    client.publish("Tzone/"+ID+'/Battary', Battary)
    client.publish("Tzone/"+ID+'/WIFI', WIFI)
    client.publish("Tzone/"+ID+'/Date', Date)
    client.publish("Tzone/"+ID+'/Time', Time)
class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print(data)
            ConvertPacketIntoElemets(binascii.hexlify(data).decode())
            print(responsePacket)
            self.send((binascii.unhexlify(responsePacket)))
            mqtt_send()
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
