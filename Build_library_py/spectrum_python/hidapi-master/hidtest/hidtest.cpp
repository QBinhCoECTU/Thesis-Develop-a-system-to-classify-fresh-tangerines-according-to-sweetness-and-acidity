
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "hidapi.h"

int main(void) {
	std::cout << "Hello" << std::endl;
	// Khởi tạo thư viện hidapi
	//hid_init();

	// Tìm kiếm thiết bị HID với Vendor ID và Product ID tương ứng
	struct hid_device_info* devs, * cur_dev;

	devs = hid_enumerate(0x0451, 0x4200);
	cur_dev = devs;

	while (cur_dev) {
		printf("Device Found\n  type: %04hx %04hx\n  path: %s\n  serial_number: %ls", cur_dev->vendor_id, cur_dev->product_id, cur_dev->path, cur_dev->serial_number);
		printf("\n");
		printf("  Manufacturer: %ls\n", cur_dev->manufacturer_string);
		printf("  Product:      %ls\n", cur_dev->product_string);
		printf("  Release:      %hx\n", cur_dev->release_number);
		printf("  Interface:    %d\n", cur_dev->interface_number);
		printf("\n");
		cur_dev = cur_dev->next;
	}
	hid_free_enumeration(devs);

	// Open the device using the VID, PID,
	// and optionally the Serial number.
	////handle = hid_open(0x4d8, 0x3f, L"12345");
	hid_device* handle = hid_open(0x0451, 0x4200, NULL);

	if (!handle) {
		printf("unable to open device\n");
		return 1;
	}

	// Giải phóng thư viện hidapi
	hid_exit();
	return 0;
}

