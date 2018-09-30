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
    def __init__(self, iq_envoy=None, pixel_count=32, ranges=(1600, 3200, 6400), grid = 800):
        self.iq_envoy = iq_envoy
        self.pixel_count = pixel_count
        self.range_boundaries = ranges
        self.range_grid = grid
        self.marker_color = (0.90, 0.20, 0.00, 0.3)
        self.bg_color = (0.0, 0.0, 0.0, 0.05)
        self.colors = {
            'produced': (0.00, 0.20, 1.00),
            'consumed': (1.00, 0.18, 0.00),
            'exported': (0.00, 1.00, 0.25)
            }
        self.saturations = [0.95, 0.97, 1.00]
        self.speeds = [3.0, 1.5, 2.0]
        self.mod_depth = 0.45
        self.mod_period = float(pixel_count) / ( 4.0 * math.pi )
        self.produced_power = 0.0
        self.consumed_power = 0.0
        self.current_range = 0
        self.current_speed = 0.0
        if self.iq_envoy is not None:
            self.iq_envoy.on_new_data = self.new_data
    
    def new_data(self, data):
        self.produced_power = data['watts_producing']
        self.consumed_power = data['watts_consuming']
        self.set_current_range()
        self.set_current_speed()

    @property
    def pixels(self):
        arr = [self.bg_color]*self.pixel_count
        if self.produced_power < self.consumed_power:
            arr = self.add_pixels_importing(arr)
        else:
            arr = self.add_pixels_exporting(arr)
        return self.convert_pixels(arr)

    def convert_pixels(self, pixels):
        return [self.convert_pixel(p) for p in pixels ]

    def convert_pixel(self, pixel):
        return int(255*pixel[0]), int(255*pixel[1]), int(255*pixel[2]), int(255*0.02) #int(255*pixel[3])

    def add_pixels_importing(self, arr):
        for i in range(self.pixel_count):
            if self.power_at_index(i) < self.produced_power:
                arr[i] = self.modulated_color(i, 'produced', True)+(0,)
            elif self.power_at_index(i) < self.consumed_power:
                arr[i] = self.modulated_color(i, 'consumed')+(0,)
        return arr

    def add_pixels_exporting(self, arr):
        for i in range(self.pixel_count):
            if self.power_at_index(i) < self.consumed_power:
                arr[i] = self.modulated_color(i, 'produced', True)+(0,)
            elif self.power_at_index(i) < self.produced_power:
                arr[i] = self.modulated_color(i, 'exported', True)+(0,)
        return arr

    def mod_gridline_pixels(self,arr):
        count = int(self.range_boundaries[self.current_range] / self.range_grid)
        for i in range(count):
            pwr = i*self.range_grid
            k = self.index_at_power(pwr)
            if k >= len(arr):
                continue
            if pwr < self.total_power:
                arr[k] = (arr[k][0:3] + (0.3,))
            else:
                arr[k] = (arr[k][0:3] + (0.1,))
        return arr

    def modulated_color(self, pixel_id, type=None, reverse=False):
        t = float(time.time())
        t = -1.0*t*reverse + t*1.0*( not reverse)
        theta = float(pixel_id) / self.mod_period
        amp = math.sin(t*self.current_speed+theta)
        amp = 1 - self.mod_depth + self.mod_depth * amp
        return self.fixed_color(type, amp)

    def fixed_color(self, type=None, amp=1.0):
        return self.hsv_color(
            color=self.colors.get(type, self.bg_color),
            sat=self.saturations[self.current_range],
            amp=amp
        )
    def set_current_speed(self):
        self.current_speed = math.ceil(self.total_power / 50) / 30

    def set_current_range(self):
        if self.total_power < self.range_boundaries[0]:
            return 0
        if self.total_power >= self.range_boundaries[-1]:
            return len(self.range_boundaries) -1
        self.current_range = [ (i,b) for (i, b)
                    in enumerate(self.range_boundaries)
                    if self.total_power<b ][-1][0]

    def index_at_power(self, pwr):
        if pwr > self.range_boundaries[self.current_range]:
            return self.pixel_count - 1
        return int(self.pixel_count * float(pwr) / self.range_boundaries[self.current_range] )

    def power_at_index(self, i):
        return self.range_boundaries[self.current_range] * float(i)/float(self.pixel_count)

    @property
    def total_power(self):
        return max(self.produced_power, self.consumed_power)

    def hsv_color(self, color=(1.0, 1.0, 1.0), amp=1.0, sat=1.0):
        hsvc = colorsys.rgb_to_hsv(*color)
        hsvc = (hsvc[0], hsvc[1]*sat, hsvc[2]*amp)
        return colorsys.hsv_to_rgb(*hsvc)



if __name__ == '__main__':
    cm = ImportExportMeter()
    print(cm.pixels)
