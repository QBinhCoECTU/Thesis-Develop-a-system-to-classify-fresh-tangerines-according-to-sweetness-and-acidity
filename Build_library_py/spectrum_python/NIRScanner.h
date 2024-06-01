//
// Created by akg on 18/06/03.
//

#ifndef NIRSCANNER_H
#define NIRSCANNER_H

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <ctime>
#include <chrono>
#include <thread>
#include <vector>
//#include <unistd.h>
#include "API.h"
#include "usb_nir.h"
#include "dlpspec.h"
#include "evm.h"
#include "NNOStatusDefs.h"

using namespace std;

class NIRScanner {
public:
    float wavelengthnir[228];
    int intensitynir[228];
    EVM mEvm;
    bool mErrorFlag;
    uint8 mPrevPGAGain;
    uScanConfig mConfig;
    void* pRefDataBlob;
    scanResults mScanResults;
    scanResults mReferenceResults;

public:
    NIRScanner(uScanConfig* pConfig = nullptr);
    ~NIRScanner();

    int readVersion();
    void resetErrorStatus();
    void setLampOnOff(int32_t newValue);
    void setConfig(uint16_t scanConfigIndex, uint8_t scan_type, uint16_t num_patterns, uint16_t num_repeats,
        uint16_t wavelength_start_nm, uint16_t wavelength_end_nm, uint8_t width_px);
    void configEVM(uScanConfig* pConfig = nullptr);
    void setPGAGain(int32_t newValue);

    string scanSNR(bool isHadamard = true);
    void scan(bool saveDataFlag = false, int numRepeats = 1);
    void copyData();
	void config_from_GUI(uint16_t wavelength_start_nm = 900, uint16_t wavelength_end_nm = 1700, uint8_t scan_type = 1, uint16_t num_repeats = 6, uint8_t width_px = 6);
    void set_element_wavelengthnir(int index, int value);
    void set_element_intensitynir(int index, int value);
    float get_element_wavelengthnir(int index);
    int  get_element_intensitynir(int index);

    string getScanData();
    int setHibernate(bool newValue);
    

private:
    int _performScanReadData(bool storeInSD, uint16 numRepeats, void* pData, int* pBytesRead);
    int _interpretData(void* pData);
};

#endif //NIRSCANNER_H

