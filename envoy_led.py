import threading
import envoy
import production_meter
import consumption_meter
import signal
import sys
import time
from neopixel import *

LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest

LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class IQEnvoyLed():
    def __init__(self):
        self.strip = Adafruit_NeoPixel(
                LED_COUNT,
                LED_PIN,
                LED_FREQ_HZ,
                LED_DMA,
                LED_INVERT,
                LED_BRIGHTNESS,
                LED_CHANNEL)
        self.strip.begin()
        self.iq_envoy = envoy.IQEnvoy()
        self.consumption_meter = consumption_meter.ConsumptionMeter(
            iq_envoy = self.iq_envoy,
            pixel_count = LED_COUNT,
            max_power = 8000
        )
        self.run = False
    def start(self):
        self.run = True
        self.set_pixels_loop()
        self.iq_envoy.start_polling()
    def stop(self):
        self.run = False
        self.iq_envoy.stop_polling()
    def set_pixels_loop(self):
        if self.run is not True:
            return
        self.set_pixels()
        threading.Timer(.05, self.set_pixels_loop).start()
    def set_pixels(self):
        for i, rgb in enumerate( self.consumption_meter.pixels ):
            self.strip.setPixelColor(i, Color(rgb[0],rgb[1], rgb[2]))
            self.strip.show()

if __name__ == '__main__':
    iqenvoy_led = IQEnvoyLed()
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        iqenvoy_led.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    iqenvoy_led.start()
    while True:
        time.sleep(1)
