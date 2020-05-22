# Sciopa--2019-2020
Team made by Tommaso Sbalchiero, Matteo Gusi, Daniele Corrini
This robot is based on a Raspberry and an Arduino. To simplify the control the real brain is Raspberry.
Due to the lack of an hardware PWM generator in the raspberry the PWM is generated by Arduino, Arduino can be easily sobstituted with a serial/SPI/I2C PWM generator, with higher frequency and resolution.
To capture the signal raspberry use 4 interrupt signal on the GPIO and the PID is calculated every 4ms. 
There is a thread which calc the PID every 1ms and it alternates the 4 channels. 
There is a little error checker to the encoder Period due to some EMI in the circuit and false captures.

Arduino communicates with the USB so there isnt' the necessity to use a level shifhter for the UART.
