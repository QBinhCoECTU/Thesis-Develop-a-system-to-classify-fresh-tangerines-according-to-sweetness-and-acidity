import NIRScanner
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
nirs = NIRScanner.NIRScanner()

#Tạo 2 mảng có 288 phần tử để sao chép dữ liệu
wavelength_array = [0 for _ in range(228)] #Mang chua gia trị bươc song
intensity_array = [0 for _ in range(228)]   #Mang lay du lieu moi lan scan

def scan_spectrum():
    nirs.readVersion()
    nirs.config_from_GUI()
    nirs.setPGAGain(16)
    nirs.scan(True, 6)
    
    #Tạo file .csv


    # time.sleep(1000)
    # nirs.config_from_GUI()
    # nirs.setPGAGain(16)
    #nirs.scan(True, 6)
    #In ra hai mảng trước khi 
    # print(wavelength_array)
    # print(intensity_array)
    
    #Sao chép dữ liệu sang hai mảng
        # wavelength_array sẽ mang các giá trị bước sóng
        # intensity_array sẽ mang các giá trị cường độ)
    for i in range(228):
        wavelength_array[i] = nirs.get_element_wavelengthnir(i)
        intensity_array[i] = nirs.get_element_intensitynir(i)
    # print(wavelength_array)
    # print(intensity_array)


if __name__ == "__main__":
    scan_spectrum()
    import csv

    # # Tạo một mảng giá trị nguyên gồm 125 giá trị
    # array = []
    # for i in range(228):
    #     array.append(i)
    # Đường dẫn và tên file CSV
    csv_file = 'sample.csv'

    # Mở file CSV để ghi với mã hóa utf-8
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Ghi dữ liệu từ mảng bước sóng vào file CSV
        for value1, value2 in zip(wavelength_array, intensity_array):
            writer.writerow([round(value1, 4), value2])
        # for value in wavelength_array:
        #     writer.writerow([value])  # Ghi dữ liệu vào cột thứ nhất
        # for value in intensity_array:

        #     writer.writerow(['' , value])  # Ghi dữ liệu vào cột thứ hai

    print("Đã tạo file CSV thành công!")

    # scan_spectrum()
    # intensity_average = np.array(intensity_array)
    # wavelength_array = np.array(wavelength_array)
    
    # intensity_average = pd.DataFrame(intensity_average)
    # wavelength_array = pd.DataFrame(wavelength_array)
    
    # intensity_average.insert(loc=0, column= 'Wavelength', value=wavelength_array)
    # intensity_average.to_csv(r"C:\Users\ADMIN\Desktop\example1\A1.csv", index=False, header=True)
    
    print(intensity_array)
    print(wavelength_array)
    
    # Vẽ biểu đồ
    plt.plot(wavelength_array, intensity_array)
    
    # Đặt tên cho trục x và trục y
    plt.xlabel("Wavelength (nm)")
    plt.ylabel('Intensity')
    # Đặt tiêu đề cho biểu đồ
    plt.title('Biểu đồ')
    # Hiển thị biểu đồ
    plt.show()

