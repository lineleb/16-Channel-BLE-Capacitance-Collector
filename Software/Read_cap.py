from machine import I2C,Pin,sleep
import ble
import bluetooth
import utime

#新建ble对象
b = bluetooth.BLE()
#导入类
p = ble.BLESimplePeripheral(b)

#创建接口
i2c0 = I2C(0, freq=100000)
i2c1 = I2C(1, freq=100000)

cap1_lsb_Add = 2  #定义寄存器地址
cap2_lsb_Add = 14
cap3_lsb_Add = 16
cap4_lsb_Add = 18

print("i2c0 scaned device:",i2c0.scan(),"\ni2c1 scaned device:",i2c1.scan())#扫描

def save_to_csv(data_list, filename):
    try:
        with open(filename, 'a') as file:
            # 获取当前时间戳
            timestamp = utime.time()
            # 将时间戳转换为时间元组
            time_tuple = utime.localtime(timestamp)
            # 构建时间字符串
            timestamp_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                time_tuple[0], time_tuple[1], time_tuple[2],
                time_tuple[3], time_tuple[4], time_tuple[5]
            )
            
            # 将时间戳和数据拼接成CSV格式的行
            csv_line = "{},{}\n".format(timestamp_str, ','.join(map(str, data_list)))
            
            # 将行写入文件
            file.write(csv_line)
            print("数据已保存到CSV文件。")
    except Exception as e:
        print("保存数据时发生错误:", e)

def calculate_crc(data):
    crc = 0xFF  # Initial value
    
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc <<= 1
            crc &= 0xFF  # Make sure the CRC remains within 8 bits
    
    return crc

i2c0.writeto(68,b'\x52\x1C'+b'\x07\xff'+calculate_crc(b'\x07\xff').to_bytes(1,'big'))#配置测量通道
sleep(1)
i2c0.writeto(68,b'\x52\x06'+b'\x0C\xff'+calculate_crc(b'\x0C\xff').to_bytes(1,'big'))#配置状态寄存器
sleep(1)

i2c0.writeto(69,b'\x52\x1C'+b'\x07\xff'+calculate_crc(b'\x07\xff').to_bytes(1,'big'))#配置测量通道
sleep(1)
i2c0.writeto(69,b'\x52\x06'+b'\x0C\xff'+calculate_crc(b'\x0C\xff').to_bytes(1,'big'))#配置状态寄存器
sleep(1)

i2c1.writeto(68,b'\x52\x1C'+b'\x07\xff'+calculate_crc(b'\x07\xff').to_bytes(1,'big'))#配置测量通道
sleep(1)
i2c1.writeto(68,b'\x52\x06'+b'\x0C\xff'+calculate_crc(b'\x0C\xff').to_bytes(1,'big'))#配置状态寄存器
sleep(1)

i2c1.writeto(69,b'\x52\x1C'+b'\x07\xff'+calculate_crc(b'\x07\xff').to_bytes(1,'big'))#配置测量通道
sleep(1)
i2c1.writeto(69,b'\x52\x06'+b'\x0C\xff'+calculate_crc(b'\x0C\xff').to_bytes(1,'big'))#配置状态寄存器
sleep(1)

i2c0.writeto(68,b'\xCC\x66')#开始测量
sleep(1)
i2c0.writeto(69,b'\xCC\x66')
sleep(1)
i2c1.writeto(68,b'\xCC\x66')
sleep(1)
i2c1.writeto(69,b'\xCC\x66')
sleep(3000)


def ReadCap(Ch_ID,Device_ID,Lsb_address):
    if Ch_ID == 0:
        i2c0.writeto(Device_ID,b'\xD2'+Lsb_address.to_bytes(1,'big'))
        Read_data = i2c0.readfrom(Device_ID,3)
        
        if calculate_crc(Read_data[0:2]) == Read_data[2]:
            Lsb = Read_data[0]
        
        i2c0.writeto(Device_ID,b'\xD2'+(Lsb_address+1).to_bytes(1,'big'))
        Read_data = i2c0.readfrom(Device_ID,3)
        
        if calculate_crc(Read_data[0:2]) == Read_data[2]:
            Msb = Read_data[0]
        
        return Msb*256+Lsb
    else:
        i2c1.writeto(Device_ID,b'\xD2'+Lsb_address.to_bytes(1,'big'))
        Read_data = i2c1.readfrom(Device_ID,3)
        
        if calculate_crc(Read_data[0:2]) == Read_data[2]:
            Lsb = Read_data[0]
        
        i2c1.writeto(Device_ID,b'\xD2'+(Lsb_address+1).to_bytes(1,'big'))
        Read_data = i2c1.readfrom(Device_ID,3)
        
        if calculate_crc(Read_data[0:2]) == Read_data[2]:
            Msb = Read_data[0]
        
        return Msb*256+Lsb

inital_value = []
inital_value.append(ReadCap(0,68,cap1_lsb_Add))
inital_value.append(ReadCap(0,68,cap2_lsb_Add))
inital_value.append(ReadCap(0,68,cap3_lsb_Add))
inital_value.append(ReadCap(0,68,cap4_lsb_Add))
inital_value.append(ReadCap(0,69,cap1_lsb_Add))
inital_value.append(ReadCap(0,69,cap2_lsb_Add))
inital_value.append(ReadCap(0,69,cap3_lsb_Add))
inital_value.append(ReadCap(0,69,cap4_lsb_Add))
inital_value.append(ReadCap(1,68,cap1_lsb_Add))
inital_value.append(ReadCap(1,68,cap2_lsb_Add))
inital_value.append(ReadCap(1,68,cap3_lsb_Add))
inital_value.append(ReadCap(1,68,cap4_lsb_Add))
inital_value.append(ReadCap(1,69,cap1_lsb_Add))
inital_value.append(ReadCap(1,69,cap2_lsb_Add))
inital_value.append(ReadCap(1,69,cap3_lsb_Add))
inital_value.append(ReadCap(1,69,cap4_lsb_Add))


Cap_value = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Delta_value = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def update_value():
    Cap_value[0] = ReadCap(0,68,cap1_lsb_Add);
    Cap_value[1] = ReadCap(0,68,cap2_lsb_Add);
    Cap_value[2] = ReadCap(0,68,cap3_lsb_Add);
    Cap_value[3] = ReadCap(0,68,cap4_lsb_Add);
    Cap_value[4] = ReadCap(0,69,cap1_lsb_Add);
    Cap_value[5] = ReadCap(0,69,cap2_lsb_Add);
    Cap_value[6] = ReadCap(0,69,cap3_lsb_Add);
    Cap_value[7] = ReadCap(0,69,cap4_lsb_Add);
    Cap_value[8] = ReadCap(1,68,cap1_lsb_Add);
    Cap_value[9] = ReadCap(1,68,cap2_lsb_Add);
    Cap_value[10] = ReadCap(1,68,cap3_lsb_Add);
    Cap_value[11] = ReadCap(1,68,cap4_lsb_Add);
    Cap_value[12] = ReadCap(1,69,cap1_lsb_Add);
    Cap_value[13] = ReadCap(1,69,cap2_lsb_Add);
    Cap_value[14] = ReadCap(1,69,cap3_lsb_Add);
    Cap_value[15] = ReadCap(1,69,cap4_lsb_Add);
    for i in range(12):
        Delta_value[i] = Cap_value[i]/inital_value[i]
    


while 1:
    if p.is_connected():
        update_value()
        print(Delta_value)
        save_to_csv(Delta_value,'data.csv')
        for i in range(12):
            Send_buffer = str(i)+','+str(Cap_value[i])+','+str(Cap_value[i]//inital_value[i])
            try:
                p.notify(Send_buffer)
            except:
                print('Can not notify')    
    utime.sleep_ms(1000)

        



