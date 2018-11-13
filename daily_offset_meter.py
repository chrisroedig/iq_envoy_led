import math
import random
import time
import colorsys

# Visualization Idea
#
#  Energy Defecit:
#  |CCCCCCC...MM......|
#
#  Energy Surplus:
#  |EEEEEEEEEEBBEE....|
#

class DailyOffsetMeter():
    def __init__(self, iq_envoy=None, pixel_count=32):
        self.iq_envoy = iq_envoy
        self.bg_color = (0.0, 0.0, 0.0, 0.05)
        self.pixel_count = pixel_count
        self.marker_position = 0.75
        self.mod_depth = 0.45
        self.mod_freq = 0.5
        self.colors = {
            'marker': (0.00, 0.20, 1.00, 0.0),
            'importing': (1.00, 0.18, 0.00, 0.0),
            'exporting': (0.00, 1.00, 0.25, 0.0)
            }
        self.offset = 0.0
        self.exporting = False
        if self.iq_envoy is not None:
            self.iq_envoy.data_callbacks.append(self.new_data)
    @property
    def pixels(self):
        arr = [self.bg_color]*self.pixel_count
        arr = self.add_offset_pixels(arr)
        arr = self.add_marker_pixels(arr)
        return self.convert_pixels(arr)
    def add_marker_pixels(self , arr):
        arr[int(math.floor(self.pixel_count*self.marker_position))] = self.colors['marker']
        arr[int(math.ceil(self.pixel_count*self.marker_position))] = self.colors['marker']
        return arr
    def add_offset_pixels(self, arr):
        top_pixel = int(math.ceil(self.offset * self.marker_position * self.pixel_count))
        for i in range(min(top_pixel, self.pixel_count)):
            arr[i] = self.fixed_color()
        arr[top_pixel] = self.modulated_color()
        return arr
    def modulated_color(self):
        amp = math.sin(self.mod_freq*time.time()*math.pi)
        amp = 1 - self.mod_depth + self.mod_depth * amp
        return self.fixed_color(amp)

    def convert_pixels(self, pixels):
        return [self.convert_pixel(p) for p in pixels ]

    def convert_pixel(self, pixel):
        return int(255*pixel[0]), int(255*pixel[1]), int(255*pixel[2]), int(255*pixel[3])

    def new_data(self, data):
        self.offset = data['wh_today_produced'] / data['wh_today_consumed']
        self.exporting = self.offset > 1.0

    def fixed_color(self, amp=1.0):
        color = self.colors['exporting'] if self.exporting else self.colors['importing']
        return self.hsv_color(
            color=color,
            sat=0.95,
            amp=amp
        )
    def hsv_color(self, color=(1.0, 1.0, 1.0), amp=1.0, sat=1.0):
        hsvc = colorsys.rgb_to_hsv(*color[0:-1])
        hsvc = (hsvc[0], hsvc[1]*sat, hsvc[2]*amp)
        return colorsys.hsv_to_rgb(*hsvc)+(color[3],)
if __name__ == '__main__':
    cm = DailyOffsetMeter()
    cm.offset = .80
    cm.exporting = False
    print(cm.pixels)
