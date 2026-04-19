/******************************************************************************
**************************Hardware interface layer*****************************
  | file        : DEV_Config.cpp
  | version     : V1.0
  | date        : 2020-06-16
  | function    : Provide the hardware underlying interface
******************************************************************************/
#include "DEV_Config.h"

/********************************************************************************
  function: System Init and exit
  note:
  Initialize the communication method
********************************************************************************/
uint8_t System_Init(void)
{
    Serial.begin(115200);
    Serial.println("USE_I2C");
    Wire.setClock(2000000);
#if defined(ARDUINO_ARCH_RP2040)
  Wire.setSDA(OLED_I2C_SDA_PIN);
  Wire.setSCL(OLED_I2C_SCL_PIN);
  Wire.begin();
#else
  Wire.begin(OLED_I2C_SDA_PIN, OLED_I2C_SCL_PIN);
#endif
    return 0;
}

/********************************************************************************
  function: Hardware interface
  note:
  I2C_Write_Byte(value, cmd):
    hardware I2C
********************************************************************************/

void I2C_Write_Byte(uint8_t value, uint8_t Cmd)
{
    uint8_t Addr = IIC_ADR;
    Wire.beginTransmission(Addr);
    Wire.write(Cmd);
    Wire.write(value);
    Wire.endTransmission();
}

/********************************************************************************
  function: Delay function
  note:
  Driver_Delay_ms(xms) : Delay x ms
  Driver_Delay_us(xus) : Delay x us
********************************************************************************/
void Driver_Delay_ms(unsigned long xms)
{
    delay(xms);
}

void Driver_Delay_us(int xus)
{
    for (int j = xus; j > 0; j--)
        ;
}