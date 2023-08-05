User needs to be in groups `spi, gpio, dialout` to be able to execute the application without sudo/root.

To enable SPI (GPIO 10) drive for the LED strip, some changes need to be made in the boot settings of the Raspberry Pi:
[rpi_ws281x library](https://github.com/jgarff/rpi_ws281x#spi)
    - namely change frequency & minimal frequency of core (cpu?) to 500 MHz and enable SPI in boot.txt
