/******************************************************************************
**************************Hardware interface layer*****************************
* | file      	:	DEV_Config.h
* |	version		  :	V1.0
* | date		    :	2020-06-16
* | function	  :	Provide the hardware underlying interface	
******************************************************************************/
#ifndef _DEV_CONFIG_H_
#define _DEV_CONFIG_H_

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <avr/pgmspace.h>

#ifndef D5
#define D5 14
#endif

#ifndef D6
#define D6 12
#endif

#ifndef OLED_I2C_SDA_PIN
#define OLED_I2C_SDA_PIN D5
#endif

#ifndef OLED_I2C_SCL_PIN
#define OLED_I2C_SCL_PIN D6
#endif
/**
 * data
**/
#define UBYTE   uint8_t
#define UWORD   uint16_t
#define UDOUBLE uint32_t

#define IIC_ADR    0X3C 
#define IIC_CMD    0X00
#define IIC_RAM    0X40

uint8_t System_Init(void);


// void DEV_SPI_WriteByte(uint8_t DATA);
void I2C_Write_Byte(uint8_t value, uint8_t Cmd);

void Driver_Delay_ms(unsigned long xms);
void Driver_Delay_us(int xus);

#endif
