import pandas as pd
import os
import numpy as np

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
            data = pd.read_csv(f)
            data = data.iloc[:, :2]
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
    srange = range(0, len(data), 228)
    for ii in srange:
        i += 228
        file = file._append(data.iloc[ii:i, 1], ignore_index=True)
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
listWavelength = data_main.values[:125, 0].tolist()
data_main = Change_shape(data_main)
data_main = pd.DataFrame(data_main)
data_main.drop(data_main.columns[125:], axis=1, inplace=True)
data_calib = pd.read_csv(r'C:\Users\ASUS\Desktop\Control_python\Calib\final_data_calibration (25-10-2023).csv')
data_calib = pd.DataFrame(data_calib)
data_calib.drop(data_calib.columns[125:], axis=1, inplace=True)
data_calib = data_calib.T
data_ref = Reference(data_calib, data_main)
final_Data = pd.DataFrame(np.array(data_ref), columns=listWavelength)

# print(final_Data, listWavelength)

#load modle

import joblib

model = joblib.load(r'C:\Users\ASUS\Desktop\Control_python\Ridge_regression.pkl')

y_pred = model.predict(final_Data)

print(y_pred[0])



