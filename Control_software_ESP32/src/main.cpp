#include <Arduino.h>
#include "L298N.h"

//link variable
TaskHandle_t Task1;
TaskHandle_t Task2;
/*Động cơ cần điều khiển tốc độ*/
// Động cơ bằng chuyền 1
#define PWM_MOTOR1 15
#define IN1_MOTOR1 4
#define IN2_MOTOR1 2

// Động cơ băng chuyền 2
#define PWM_MOTOR2 18
#define IN1_MOTOR2 13
#define IN2_MOTOR2 19

// Động cơ xoay quýt
#define PWM_MOTOR3 27
#define IN1_MOTOR3 21
#define IN2_MOTOR3 22

/*Xilanh điện ko cần điều khiển tốc độ*/
//Xilanh điện 1
#define IN1_CYLINDER1 17
#define IN2_CYLINDER1 5
// //xilanh điện 2
#define IN1_CYLINDER2 16
#define IN2_CYLINDER2 33
// //Xilanh điện 3
#define IN1_CYLINDER3 23
#define IN2_CYLINDER3 26
//Công tắc hành trình
#define CTHT 25
//Cảm biến tiệm cận
#define SENSOR1 36
#define SENSOR2 34
#define SENSOR3 32

L298N motor1(IN1_MOTOR1, IN2_MOTOR1);
L298N motor2(IN1_MOTOR2, IN2_MOTOR2);
L298N motor3(IN1_MOTOR3, IN2_MOTOR3);

L298N cylinder1(IN1_CYLINDER1, IN2_CYLINDER1);
L298N cylinder2(IN1_CYLINDER2, IN2_CYLINDER2);
L298N cylinder3(IN1_CYLINDER3, IN2_CYLINDER3);

uint16_t mytime = 700;
uint8_t ledstatus = 0;
bool mystop = true;
bool mystop1 = true;
bool mystop2 = true;
uint8_t status_xl1 = 0;
uint8_t loaiquyt = 0;
uint8_t process = 1;
uint8_t process1 = 1;
uint8_t process2 = 1;
uint8_t process3 = 1;
// put function declarations here:
void checkcylinder();
void setSpeedMotor_1(int duty);
void setSpeedMotor_2(int duty);
void setSpeedMotor_3(int duty);
String data;
char dulieu;

void task2(void *pvParameters) {
  while (1) {
    motor2.forward();
    if(digitalRead(SENSOR2) == 0 && loaiquyt == 1){
      delay(1000);
      motor2.stop();
      cylinder2.forward();
      delay(1200);
      cylinder2.backward();
      delay(1200);
      motor2.backward();
    }

    if(digitalRead(SENSOR3) == 0 && loaiquyt == 2){
      delay(650);
      motor2.stop();
      cylinder3.forward();
      delay(1200);
      cylinder3.backward();
      delay(1200);
      motor2.backward();
    }
    vTaskDelay(5);
  }
}

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
  //Cấu hình cảm biến tiệm cận và công tắc hành trình
  pinMode(SENSOR1, INPUT);
  pinMode(SENSOR2, INPUT);
  pinMode(SENSOR3, INPUT);
  pinMode(CTHT, INPUT);

  // Initialize channels
  // channels 0-15, resolution 1-16 bits, freq limits depend on resolution
  // ledcSetup(uint8_t channel, uint32_t freq, uint8_t resolution_bits);
  ledcSetup(1, 12000, 8); // 12 kHz PWM, 8-bit resolution
  ledcSetup(2, 12000, 8);
  ledcSetup(3, 12000, 8);

  // assign motor speed pins to channels
  ledcAttachPin(PWM_MOTOR1, 1);
  ledcAttachPin(PWM_MOTOR2, 2);
  ledcAttachPin(PWM_MOTOR3, 3);

  setSpeedMotor_1(255);
  setSpeedMotor_2(240);
  setSpeedMotor_3(215);

  xTaskCreatePinnedToCore(
    task2,              // Function to run on Core 0
    "Task2",            // Name of the task
    10000,              // Stack size (bytes)
    NULL,               // Task parameters
    1,                  // Priority
    &Task2,             // Task handle
    0                   // Core to run the task on (Core 0)
  );
}

void loop()
{
  if(Serial.available() > 0) //Cho du lieu
  {
    dulieu = Serial.read();
    // dulieu.trim();
    if(dulieu == 's') //Bat dau chay he thong
    {
      while(mystop){
        if(process1 == 1){
          motor1.forward();
          if(digitalRead(SENSOR1) == 0){
          delay(600);// Delay mot khoang cho toi can day
          motor1.stop();
          process1 = 2;
          }
        }

        if(process1 == 2){
          if(digitalRead(CTHT) == 1){
            cylinder1.forward();
            motor3.forward();
            status_xl1 = 1;
          }
          if(digitalRead(CTHT) == 0 && status_xl1 == 1){
            cylinder1.stop();
            motor3.stop();
            Serial.println("1");
            process1 = 1;

            mystop = false;
          }
        }

        // if(mystop == 1){
        //   mystop = 0;
        //   break;
        // }
        // vTaskDelay(1);
      }
    }

    if(dulieu == '2')
    {
      while(mystop1){
        //Nhich ra mot chut xoay
        if(process2 == 1){
          cylinder1.backward();
          delay(mytime);
          cylinder1.stop();
          motor3.forward();
          delay(540);
          //----------Chuong trinh xoay--------------
          //  delay(2000);
          //---------------------
          process2 = 2;
        }
        //Đẩy vào đụng ctht va gui tin hieu lay du lieu
        if(process2 == 2){
          if(digitalRead(CTHT) == 1){
            cylinder1.forward();
            motor3.forward();
            status_xl1 = 1;
          }
          if(digitalRead(CTHT) == 0 && status_xl1 == 1){
            cylinder1.stop();
            motor3.stop();
            Serial.println("1");

            process2 = 1;
            mystop1 = false;
          }
        }
      }
    }

    if(dulieu == '3')
    {
      while(mystop2){
        //Nhich ra mot chut Xoay quýt 120 độ
        if(process3 == 1){
          cylinder1.backward();
          delay(mytime);
          cylinder1.stop();
          motor3.forward();
          delay(500);
          //Chuong trinh xoay--------------
          // delay(2000);
          //---------------------
          process3 = 2;
        }
        //Đẩy vào đụng ctht va gui tin hieu lay du lieu
        if(process3 == 2){
          if(digitalRead(CTHT) == 1){
            cylinder1.forward();
            motor3.forward();
            status_xl1 = 1;
          }
          if(digitalRead(CTHT) == 0 && status_xl1 == 1){
            cylinder1.stop();
            motor3.stop();
            Serial.println("1");
            process3 = 1;
            mystop2 = false;
          }
        }
      }
    }

    if(dulieu == 'A')
    {
      loaiquyt = 1;
      cylinder1.backward();
      delay(2300);
      mystop = true;
      mystop1 = true;
      mystop2 = true;
      Serial.println("a");
    }

    if(dulieu == 'B'){
      loaiquyt = 2;
      cylinder1.backward();
      delay(2300);
      mystop = true;
      mystop1 = true;
      mystop2 = true;
      Serial.println("a");
    }

    if(dulieu == 'C')
    {
      loaiquyt = 3;
      cylinder1.backward();
      delay(2300);
      mystop = true;
      mystop1 = true;
      mystop2 = true;
      Serial.println("a");
    }

    if(dulieu == 'v') cylinder1.backward();
  }
  // vTaskDelay(1);
}

// put function definitions here:

// // Chương trình kiểm tra xilanh điện
void checkcylinder(void){
  // cylinder1.forward();
  cylinder2.forward();
  cylinder3.forward();
  delay(200);
  // cylinder1.stop();
  cylinder2.stop();
  cylinder3.stop();
  delay(500);
  // cylinder1.forward();
  cylinder2.forward();
  cylinder3.forward();
  delay(200);
  // cylinder1.stop();
  cylinder2.stop();
  cylinder3.stop();
  delay(500);// cylinder1.forward();
  cylinder2.forward();
  cylinder3.forward();
  delay(200);
  // cylinder1.stop();
  cylinder2.stop();
  cylinder3.stop();
  delay(500);
  // cylinder1.backward();
  cylinder2.backward();
  cylinder3.backward();
  delay(2000);
}

void setSpeedMotor_1(int duty){
  ledcWrite(1, duty);
}

void setSpeedMotor_2(int duty){
  ledcWrite(2, duty);
}

void setSpeedMotor_3(int duty){
  ledcWrite(3, duty);
}

