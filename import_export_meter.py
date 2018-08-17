import math
import random
import time
import colorsys

# Visualization Idea
#
#  Importing Power:
#  |>>>>>>><<<<<<<<<<#-----------|
#  |  blue |  amber  |   bg      |
#
#  Exporting Power:
#  |>>>>>>>>>#>>>>>>>>>----------|
#  |   blue  |  green |  bg      |
#
#

class ImportExportMeter():
    def __init__(self, iq_envoy=None, pixel_count=32, ranges=(1600, 3200, 6400)):
        self.iq_envoy = iq_envoy
        self.pixel_count = pixel_count
        self.range_boundaries = ranges
        self.marker_color = (1.00, 1.00, 1.00)
        self.bg_color = (0.10, 0.10, 0.10)
        self.colors = {
            'produced': (0.00, 0.40, 1.00),
            'consumed': (1.00, 0.18, 0.00),
            'exported': (0.00, 1.00, 0.58)
            }
        self.saturations = [0.50, 0.75, 1.00]
        self.speeds = [2.0, 3.0, 4.0]
        self.mod_depth = 0.4
        self.mod_period = float(pixel_count) / ( 16.0 * math.pi )

    def pixels_importing(self):
        arr = [self.bg_color]*self.pixel_count
        for i in range(self.pixel_count):
            print self.power_at_index(i)
            if self.power_at_index(i) < self.produced_power:
                arr[i] = self.modulated_color(i, 'produced')
            elif self.power_at_index(i) < self.consumed_power:
                arr[i] = self.modulated_color(i, 'consumed', True)
        arr[self.index_at_power(self.consumed_power)] = self.marker_color
        return arr


    def fixed_color(self, type=None, amp=1.0):
        return self.hsv_color(
            color=self.colors.get(type, self.bg_color),
            sat=self.saturations[self.current_range],
            amp=amp
        )
    def modulated_color(self, pixel_id, type=None, reverse=False):
        t = float(time.time())
        t = -1*t*reverse + t*( not reverse)
        theta = float(pixel_id) / self.mod_period
        amp = math.sin(t*self.speeds[self.current_range]+theta)
        amp = 1 - self.mod_depth * amp
        return self.fixed_color(type, amp)

    @property
    def current_range(self):
        if self.total_power < self.range_boundaries[0]:
            return 0
        return [ (i,b) for (i, b)
                    in enumerate(self.range_boundaries)
                    if self.total_power<b ][-1][0]

    def index_at_power(self, pwr):
        return int(self.pixel_count * float(pwr) / self.range_boundaries[self.current_range] )
    def power_at_index(self, i):
        return self.range_boundaries[self.current_range] * float(i)/float(self.pixel_count)
    @property
    def total_power(self):
        return max(self.produced_power, self.consumed_power)

    @property
    def consumed_power(self):
        return self.get_consumed_power()

    @property
    def produced_power(self):
        return self.get_produced_power()

    def get_consumed_power(self):
        return 4000
    def get_produced_power(self):
        return 900

    def hsv_color(self, color=(1.0, 1.0, 1.0), amp=1.0, sat=1.0):
        hsvc = colorsys.rgb_to_hsv(*color)
        hsvc = (hsvc[0], hsvc[1]*sat, hsvc[2]*amp)
        return colorsys.hsv_to_rgb(*hsvc)



if __name__ == '__main__':
    cm = ImportExportMeter()
    print cm.pixels
