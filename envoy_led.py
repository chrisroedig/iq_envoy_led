import threading
import envoy
import production_meter
import signal
import sys
import time
from neopixel import *

LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest

LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

class IQEnvoyLed():
    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
            LED_STRIP)
        self.iq_envoy = envoy.IQEnvoy(ip_address = '192.168.1.68')
        self.production_meter = production_meter.ProductionMeter(
            iq_envoy = self.iq_envoy,
            pixel_count = LED_COUNT,
            max_power = 5000
        )
        self.run = False
    def start(self):
        self.run = True
        self.iq_envoy.start_polling()
        self.set_pixels_loop()
    def stop(self):
        self.run = False
        self.iq_envoy.stop_polling()
    def set_pixels_loop(self):
        if self.run is not True:
            return
        self.set_pixels()
        threading.Timer(1.00, self.set_pixels_loop).start()
    def set_pixels(self):
        for i, color in enumerate( self.production_meter.pixels ):
            self.strip.setPixelColor(i, color)
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
