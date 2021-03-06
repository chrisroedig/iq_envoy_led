import threading
import envoy
import import_export_meter
import daily_offset_meter
import signal
import sys
import time
import datetime
from neopixel import *

LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 64     # Set to 0 for darkest and 255 for brightest

LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812_STRIP_RGBW


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
        self.strip.begin()
        self.iq_envoy = envoy.IQEnvoy()
        self.exim_meter = import_export_meter.ImportExportMeter(
            iq_envoy = self.iq_envoy,
            pixel_count = LED_COUNT
        )
        self.doffset_meter = daily_offset_meter.DailyOffsetMeter(
            iq_envoy = self.iq_envoy,
            pixel_count = LED_COUNT
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
        threading.Timer(.025, self.set_pixels_loop).start()
    def set_pixels(self):
        pixels = self.pixel_source().pixels 
        for i, rgb in enumerate( pixels ):
            self.strip.setPixelColor(i, Color(rgb[1],rgb[0], rgb[2],rgb[3]))
        self.strip.show()
    def pixel_source(self):
        seconds = datetime.datetime.now().second
        if (seconds % 20) < 10:
            return self.exim_meter
        else:
            return self.doffset_meter



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
