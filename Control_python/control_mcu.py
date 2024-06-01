# khai báo thư viện random
import random

import serial #for Serial communication
import time   #for delay functions
import NIRScanner
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

nirs = NIRScanner.NIRScanner()

#Tạo 2 mảng có 288 phần tử để sao chép dữ liệu
wavelength_array = [0 for _ in range(228)] #Mang chua gia trị bước song
intensity_array = [0 for _ in range(228)]   #Mang lay du lieu moi lan scan

# Cấu hình cảm biến nir
nirs.readVersion()
nirs.config_from_GUI()
nirs.setPGAGain(16)

def scan_spectrum():
    nirs.setPGAGain(16)
    nirs.scan(True,6)
    #Sao chép dữ liệu sang hai mảng
        # wavelength_array sẽ mang các giá trị bước sóng
        # intensity_array sẽ mang các giá trị cường độ)
    for i in range(228):
        wavelength_array[i] = nirs.get_element_wavelengthnir(i)
        intensity_array[i] = nirs.get_element_intensitynir(i)

serial.Serial("COM3", 115200).close()
ser = serial.Serial('COM3', 115200)
#Truyền giá trị cho esp32
def Serialwrite(s):
    ser.write(s.encode())

#Đọc giá trị từ esp32
def Serialread():
    ser.readline().decode()
    # ser.readline(s1.decode())
times = 1


# in random giá trị từ thanh phần
loai = [1, 2, 3]

# Serialwrite('v') #Bat dau chay he thong
# time.sleep(2000) 
Serialwrite('s') #Bat dau chay he thong

while True:
    # s = str(input())
    
    #  #Truyền giá trị cho esp32
    # Serialwrite(s)
    
    response = ser.readline().decode()
    print("Received response:", response)
    con = response.strip()
    
    if con == "1":
        scan_spectrum()
        print("Scaned")
        intensity_average = np.array(intensity_array)
        wavelength_array = np.array(wavelength_array)  

        intensity_average = pd.DataFrame(intensity_average)
        wavelength_array = pd.DataFrame(wavelength_array)
        print(intensity_array)
        print(wavelength_array)
        #Ket thuc qua trinh trinh lay du lieu
        
        """
        #   Doan code chay mo hinh
        
        """
        
        value = random.choice(loai)
        # Truyen gia tri ve esp32
        if(value == 1):
            Serialwrite("A") # Loai 1
        if(value == 2):
            Serialwrite("B") # Loai 1
        if(value == 3):
            Serialwrite("C") # Loai 1
        
        print("end scan")
        print(value)
    if(con == 'a'):
        Serialwrite('s')

