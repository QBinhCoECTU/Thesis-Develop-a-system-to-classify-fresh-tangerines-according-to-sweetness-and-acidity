import os
import random
import serial #for Serial communication
import time   #for delay functions
import NIRScanner
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib


nirs = NIRScanner.NIRScanner()

#Tạo 2 mảng có 288 phần tử để sao chép dữ liệu
wavelength_array = [0 for _ in range(228)] #Mang chua gia trị bươc song
intensity_array = [0 for _ in range(228)]   #Mang lay du lieu moi lan scan

# Cấu hình cảm biến nir
nirs.readVersion()
nirs.config_from_GUI()
nirs.setPGAGain(16)

def Get_data(path):
    """
    :param path: Thư mục chứa các file csv từ cảm biến
    :return: Trả về tên file và giá trị trong file
    """
    os.chdir(path)
    files = sorted(os.listdir(path))
    name_csv = []
    try:
        for f in files:
            if f.endswith('.csv'):
                name_csv.append(f)
        df = pd.DataFrame()
        for f in name_csv:
            data = pd.read_csv(f, skiprows=[i for i in range(0, 21)])
            df = df._append(data)

    except:
        pass 
    return name_csv, df


def Change_shape(data):
    """
    :param data: Chunky đổi shape của giá trị từ dọc thành ngang
    :return: trả về dataframe chứa các giá trị đã chuyển
    """
    file = pd.DataFrame()
    i = 0
    srange = range(0, len(data['Sample Signal (unitless)']), 228)
    for ii in srange:
        i += 228
        file = file._append(data.iloc[ii:i, 3], ignore_index=True)
    return file


def Reference(calib_data, signal_data):

    """
    :param calib_data: Nhập giá trị từ file calibration (Final.... .cvs)
    :param signal_data: Nhập giá trị cột signal của file csv cảm biến
    :return: Giá trị đã tính toán với công thức là signal/calib
    """
    bien_dem = 0
    values_calib = []
    values_calib_2 = []
    for list_sig_data in signal_data.values:
        for sig_data in list_sig_data:
            for clib in calib_data.values[bien_dem]:
                ref_data = sig_data / clib
                values_calib.append([ref_data])
            bien_dem = bien_dem + 1
        bien_dem = 0
        values_calib = pd.DataFrame(values_calib).T
        values_calib_2 = pd.DataFrame(values_calib_2)._append([values_calib])
        values_calib = []
    return values_calib_2

name_data, data_main = Get_data(r'C:\Users\ASUS\Desktop\Control_python')

listWavelength = data_main.values[0:125, 0].tolist()
data_main = Change_shape(data_main)
data_main = pd.DataFrame(data_main)
data_main.drop(data_main.columns[125:], axis=1, inplace=True)

data_calib = pd.read_csv(r'C:\Users\ASUS\Desktop\Control_python\Calib\final_data_calibration (25-10-2023).csv')
data_calib = pd.DataFrame(data_calib)
data_calib.drop(data_calib.columns[125:], axis=1, inplace=True)
data_calib = data_calib.T
data_ref = Reference(data_calib, data_main)
final_Data = pd.DataFrame(np.array(data_ref), columns=listWavelength)

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
times = 1

#random giá trị
loai = [1, 2, 3]

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
        name_data, data_main = Get_data(r'C:\Users\ASUS\Desktop\Control_python')

        listWavelength = data_main.values[0:125, 0].tolist()
        data_main = Change_shape(data_main)
        data_main = pd.DataFrame(data_main)
        data_main.drop(data_main.columns[125:], axis=1, inplace=True)

        data_calib = pd.read_csv(r'C:\Users\ASUS\Desktop\Control_python\Calib\final_data_calibration (25-10-2023).csv')
        data_calib = pd.DataFrame(data_calib)
        data_calib.drop(data_calib.columns[125:], axis=1, inplace=True)
        data_calib = data_calib.T
        data_ref = Reference(data_calib, data_main)
        final_Data = pd.DataFrame(np.array(data_ref), columns=listWavelength)

        # print(final_Data)

        # Mảng đa chiều để load vào modle
        X = final_Data

        #load modle

        model = joblib.load(r'C:\Users\ASUS\Desktop\Control_python\Ridge_regression.pkl')

        y_pred = model.predict(X)

        # print(y_pred[0])

        value = random.choice(loai)
        # Truyen gia tri ve esp32
        if(value == 1 ):
            Serialwrite("A") # Loai 1
            
        if(value == 2):
            Serialwrite("B") # Loai 1
        if(value == 3):
            Serialwrite("C") # Loai 1
        
        print("end scan")
        print(y_pred[0])

    if(con == 'a'):
        Serialwrite('s')

