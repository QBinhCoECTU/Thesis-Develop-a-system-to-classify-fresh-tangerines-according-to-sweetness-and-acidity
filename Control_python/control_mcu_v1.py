import serial #for Serial communication
import time   #for delay functions
import NIRScanner
import pandas as pd
import numpy as np


nirs = NIRScanner.NIRScanner()

#Tạo 2 mảng có 288 phần tử để sao chép dữ liệu
wavelength_array = [0 for _ in range(228)] #Mang chua gia trị bươc song
intensity_array = [0 for _ in range(228)]   #Mang lay du lieu moi lan scan

# Cấu hình cảm biến nir
nirs.readVersion()
nirs.config_from_GUI()
nirs.setPGAGain(16)

def scan_spectrum():
    nirs.scan(True,6)
    #Sao chép dữ liệu sang hai mảng
        # wavelength_array sẽ mang các giá trị bước sóng
        # intensity_array sẽ mang các giá trị cường độ)
    for i in range(228):
        wavelength_array[i] = nirs.get_element_wavelengthnir(i)
        intensity_array[i] = nirs.get_element_intensitynir(i)


ser = serial.Serial('COM3', 115200) 

#Truyền giá trị cho esp32
def Serialwrite(s):
    ser.write(s.encode())

#Đọc giá trị từ esp32
def Serialread():
    ser.readline().decode()
    # ser.readline(s1.decode())

times = 0

Serialwrite('s') #Bat dau chay he thong

while True:
    # s = str(input())
    
    #  #Truyền giá trị cho esp32
    # Serialwrite(s)
    
    response = ser.readline().decode()
    print("Received response:", response)
    con = response.strip()

    if(con == "1"):
        scan_spectrum()
        print("Scaned")
        intensity_average = np.array(intensity_array)
        wavelength_array = np.array(wavelength_array)

        intensity_average = pd.DataFrame(intensity_average)
        wavelength_array = pd.DataFrame(wavelength_array)
        print(intensity_array)
        print(wavelength_array)
        #Ket thuc qua trinh trinh lay du lieu
        
        times = times + 1
        
        if(times == 1):
            Serialwrite("2")
        if(times == 2):
            Serialwrite("3")

        print("times = ", times)

        if(times == 3):
            #Reset số lần đo
            times = 0
            """
            # Doan code chay mo hinh

            Load model
            Load model chuẩn hóa
            Lấy dữ liệu
            Tiền xử lý dữ liệu (lúc chuẩn bị dữ liệu để train sao thì làm lại y gan vậy)
            Đưa dữ liệu vào model

            """
            #Trả về dữ kết quả phân loại tương ứng

            Serialwrite("A") # Loai 1

            # Serialwrite("B") # Loai 2
            # Serialwrite("C") # Loai 3

    if(con == 'a'):
        Serialwrite('s')
