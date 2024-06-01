#ifndef _BLINK_H_
#define _BLINK_H_

#include "Arduino.h"

#define LED 13
#define LED_RED 32
#define LED_GREEN 33
#define LED_BLUE 25

void ledrgboff(void);
void RGB_LED(uint8_t red, uint8_t green, uint8_t blue);
void blink(void);
void setblink(void);
void ledcolor(uint8_t color, uint8_t status);

#endif