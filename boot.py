



import lib,ubinascii,time,machine,dht,socket,re,gc,network,_thread,network,led_time 
from robust import MQTTClient
from lib import getPin 
from machine import Pin,RTC,UART,WDT 
from urequests import get 
from utime import sleep 
import utime as time 
import utime,ujson,urequests,lib 
wdt = WDT(timeout=25000)
lib.wifi("PDCN","1234567788")
#http://myxw94.cn/tools/t/?key=9527&th=123jhl
# Default MQTT server to connect to
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import webrepl
webrepl.start()
from machine import UART
uart = UART(2,baudrate=38400,rx=23,tx=22,timeout=10)
led=[32,27,26,25]
WDT(timeout=15000)
led_sw=1
btn=Pin(0,Pin.IN)
btn.irq(handler=lambda fm_s:pin(21,0) if pin(21,2) else pin(21,1),trigger=(Pin.IRQ_FALLING and Pin.IRQ_RISING))
pin_s={}#保存PIN状态


def send(t):
  uart.write(t)
  sleep(1)
  resp=uart.read()
  print ("REC:",t,"RESP:",resp)
  if resp!=None:
      return resp
  return b"err"

lib.wifi("PDCN","1234567788")
#####/#######
#全局变量
global c,subtopic,pubtopic
ds=1
#####/#######
def run():
  #######################
  global singal

  while 1:
    if singal != 0:
      pin(23,1)
      limit=120
      if singal >limit:
        singal=limit
      print (singal)
      step.SteperRun(singal)
      pin(23,0)
      time.sleep(1)
      step.init([25,26,27,14],2)
      step.SteperRun(singal*-1)
      singal=0
def dht11(_pin):
  pin(13,1)
  d=dht.DHT11(machine.Pin(_pin))
  a=[]
  try:
      d.measure()
      a=[d.temperature(),d.humidity()]
      pin(13,0)
  except Exception as e:
       print (e)
       a=[99,99]
       pass
  return a

def collect():
      from urequests import get
      TH=dht11(17)
      print (TH[0],TH[1])
      url="http://myxw94.cn/tools/t/?key=9527&th="+str(TH[0])+"-"+str(TH[1])
      get(url)
      print ("已收集,%s,%s"%(TH[0],TH[1]))


#gpio 控制的引脚


#st 引脚的值


def pin(gpio=2,st=1):
    global pin_s
    if st==1:
        Pin(gpio,Pin.OUT).value(1)
        pin_s[gpio]=1
    elif st==0:
        Pin(gpio,Pin.OUT).value(0)
        pin_s[gpio]=0
    elif st==2:
        try: 
          return pin_s[gpio]
        except:
          pin_s[gpio]=0
          return 1
       


def collect():
      TH=dht11(17)
      print (TH[0],TH[1])
      url="http://myxw94.cn/tools/t/?key=9527&th="+str(TH[0])+"-"+str(TH[1])
      get(url)
def wd():
      led_time.disp_number(dht11(17)[0]*100)
      led_time.set_digit(0,412)
      led_time.set_digit(1,198)


def getInfo(auth,type_="light"):


    #获取信息


    # 电灯"&miType=light"


    #插座"&miType=outlet"


    #多个插座"&miType=multi_outlet"


    #传感器&miType=sensor"


    #设置设备类型


    host = 'https://iot.diandeng.tech'


    url = '/api/v1/user/device/diy/auth?authKey=' + auth + "&miType="+type_+"&version=1.2.2"
    print (host ,url)
    data =  ujson.loads(urequests.get(host + url).text)

    ''' deviceName = data['detail']['deviceName'] iotId =
    data['detail']['iotId'] iotToken = data['detail']['iotToken']
    productKey = data['detail']['productKey'] uuid =
    data['detail']['uuid'] broker = data['detail']['broker']] '''
    return data


def sub_cb(topic, msg):
#回调函数，收到服务器消息后会调用这个函数
#所以制模块的代码

    global led_sw
    for a in led:
      pin(a,1)
    print("[",utime.time(),"]Mqtt接收<<<<",msg)
    msg=ujson.loads(msg)
    msgs=str(msg)

    if msgs.find("MIOT")!=-1:
       MI(msg)


    if msgs.find("fm-sw")!=-1:
      if(pin(21,2)):
          pin(21,0)
          c.publish(pubtopic,playload({"fm-sw":{ "col":"#000000"}}) )


      else:


          pin(21,1)


          c.publish(pubtopic,playload({"fm-sw":{ "col":"#99FF99"}}) )





    #换频道





    if (msgs.find("fm-fre")!=-1):


       fm_res=send("AT+CH="+"%02d" % msg['data']['fm-fre'])


       c.publish(pubtopic,playload({"fre-text":{ "tex":"FRE:"+str(fm_res)}}) )
    #调音量

    if msgs.find("fm-vol")!=-1:
       fm_res=send("AT+VOL="+str("%02d" % msg['data']['fm-vol']))

    #搜台
    if msgs.find("fm-search")!=-1:
       resp=send("AT+SCAN")

       c.publish(pubtopic,playload("Searching..."))

    if msgs.find("AT")!=-1:
       print(str(msg['data']))
       send(str(msg['data']))
       c.publish(pubtopic,playload("Waing resp in console..."))

    if msgs.find("temp")!=-1:
       if led_sw==1:
         led_sw=0
       else:
         led_sw=1
       TH=dht11(17)
       c.publish(pubtopic,playload({"temp":{ "tex":str(TH[0])}}))
       c.publish(pubtopic,playload({"humi":{ "tex":str(TH[1])}}))
    #APP心跳回复
    c.publish(pubtopic,playload({"state":"online"}))
    for a in led:
      pin(a,0)




#处理小爱响应


def MI(msg):
  try:

    if(msg['data']['get']=="state"):
      if devTpye=="sensor":
        TH=dht11(17)
        c.publish(pubtopic,playload({"temp":TH[0],"humi":TH[1], "pm25":"10","co2":"10"},toDevice="MIOT_r",deviceType="vAssistant"))
        pass
      if devTpye=="light":
        pin_State= "True" if pin(21,2)==0 else "False"
        c.publish(pubtopic,playload({"pState":pin_State,"col":0,"clr":0,"mode":0,"colTemp":"1000","bright":"1"},toDevice='MIOT_r',deviceType='vAssistant'))


  except:


    pass


  #作为电灯时的操作


  try:


    if(msg['data']['set']['pState']==1):


        pin(21,1)


        print("开启")








    if(msg['data']['set']['pState']==0):
        pin(21,0)
        print ("关闭")
    #获取电源状态，操作完毕回复小爱
    pin_State= "True" if pin(21,2)==0 else "False"
    c.publish(pubtopic,playload({"pState":pin_State},toDevice='MIOT_r',deviceType='vAssistant'))
  except:
    pass
  try:
    vol=int(msg['data']['set']['bright'])*0.3
    fm_res=send("AT+VOL="+str("%02d" % vol))
    c.publish(pubtopic,playload({"bright":str(msg['data']['set']['bright'])},toDevice='MIOT_r',deviceType='vAssistant'))
  except:
    pass
  print ("已回复小爱")

key='60975280bf3e'
# 电灯"light"
#插座"outlet"
#多个插座"multi_outlet"


#传感器"sensor"


#设置设备类型


devTpye="light"


info=  getInfo(key,type_=devTpye)


lib.update_time() #更新时间


singal=0





def playload(msg,toDevice=info['detail']['uuid'],deviceType='OwnApp'):


   _data= ujson.dumps({


   'fromDevice': info['detail']['deviceName'] ,
   'toDevice':   toDevice,
   'data':       msg ,
   'deviceType': deviceType})
   print ("[",utime.time(),"]Mqtt发送>>>>",_data)
   return _data

def mqtt():
  global c,subtopic,pubtopic,led_sw
  SERVER = "public.iot-as-mqtt.cn-shanghai.aliyuncs.com"
  USER=info['detail']['iotId']
  PWD=info['detail']['iotToken']
  CLIENT_ID =  info['detail']['deviceName']
  c=MQTTClient(client_id=CLIENT_ID,server=SERVER,user=USER,password=PWD,keepalive=300)
  c.DEBUG = True
  c.set_callback(sub_cb)
  subtopic="/"+info['detail']['productKey']+"/"+info['detail']['deviceName']+"/r"
  pubtopic=b"/"+info['detail']['productKey']+"/"+info['detail']['deviceName']+"/s"
  print("user:",USER,"CLIENT_ID:",CLIENT_ID,subtopic,"/r",pubtopic)
  if not c.connect(clean_session=False):
      print("Ne session being set .")
      c.subscribe(subtopic)
  c.publish(pubtopic,"System Started!")

  for a in range(1,5):
       sleep(1)
       lib.bb(5)
  timer=0
  #LED初始化
  led_time.initialize(1)
  led_flag=0
  while 1:
    time.sleep(1)
    if led_sw==1:
       # print ("led",led_flag)
        pin(led[led_flag],0)
        led_flag+=1
        if led_flag==4:
            led_flag=0
        pin(led[led_flag],1)
    else:
      for aa in led:
        pin(aa,0)
    #喂狗
    WDT().feed()
    c.check_msg()
    resp=uart.read()
    if resp!=None:
        c.publish(pubtopic,playload(str(resp)))
    #循环时间变量
    _time=RTC().datetime()
    #oled屏幕时间
    led_time.showDots(1) if timer%2==1 else led_time.showDots(0)
    led_time.disp_number(int(str(_time[4])+(str(_time[5]) if _time[5] >9 else '0'+str(_time[5]))))
    c.check_msg()

    timer+=1
    if timer%5==0:
        wd()
        led_time.showDots(0)
        time.sleep(0.3)
    if ds==1:
          #每天更新网络时间
          if _time[4]==2 and _time[5]==1 and _time[6]==1:
              #到点重启
              machine.reset()
          #整点
          if _time[5]==1 and _time[6]==1:
            lib.bb(5)
            time.sleep(1)
            lib.bb(5)
            time.sleep(1)
            lib.bb(5)
            lib.update_time()
          #半点
          if _time[5]==30 and _time[6]==1:
            lib.bb(14,f=500)
            time.sleep(1)
            lib.bb(14,f=500)
            time.sleep(1)
            lib.bb(14,f=500)
          if _time[4]==7 and _time[5]==50 and _time[6]==1:
            uart.write("AT+FRE=1046")
            pin(16,0)
          if _time[4]<6:


            led_sw=0


    #TH=dht11(17)


    #print("温度:%s,湿度%s"%(TH[0],TH[1]))


    #断网重启


    if not network.WLAN(network.STA_IF).isconnected():


        print('断网重启...')


        lib.bb(5)
        lib.bb(5)
        lib.bb(5)
        lib.bb(5)
        lib.bb(5)
        machine.reset()
_thread.start_new_thread(mqtt,())
#_thread.start_new_thread(run,())



