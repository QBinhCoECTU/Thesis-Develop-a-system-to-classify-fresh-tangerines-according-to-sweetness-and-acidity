import csv

# Hai mảng đầu vào
array1 = [1, 2, 3, 4, 5]
array2 = ['a', 'b', 'c', 'd', 'e']

# Đường dẫn và tên file .csv
file_path = "getdata.csv"

# Mở file .csv để ghi
with open(file_path, mode='w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)

    # Ghi tiêu đề cột (nếu cần)
    writer.writerow(['Colum2', 'Colum1'])

    # Ghi giá trị từ hai mảng vào từng hàng
    for value1, value2 in zip(array1, array2):
        writer.writerow([value1, value2])

