import ble
import bluetooth
import utime
#新建ble对象
b = bluetooth.BLE()
#导入类
p = ble.BLESimplePeripheral(b)
#查看mac地址，能正常显示mac地址就是创建广播成功
aa=b.config('mac')
print('mac地址为')
print(aa)
#接受数据函数
def on_rx(v):
    print(v)
    print("Receive_data:", str(v))

p.on_write(on_rx)

while 1:
    if p.is_connected():
        p.notify('2,120.456')   #发送数据（以通知形式）
    utime.sleep_ms(1000)
    
#运行之后打开手机ble助手，连接即可，默认id：mpyble，可在ble.py中更改
