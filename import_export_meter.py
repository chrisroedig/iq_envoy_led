import math
import random
import time
import colorsys

# Visualization Idea
#
#  Importing Power:
#  |PPPPPPPP<C<C<C<C<C|
#
#  Exporting Power:
#  |PPPPPPPPP>E>E>E>E>|

class ImportExportMeter():
    def __init__(self, iq_envoy=None, pixel_count=32):
        self.iq_envoy = iq_envoy
        self.pixel_count = pixel_count
        self.bg_color = (0.0, 0.0, 0.0, 0.05)
        self.colors = {
            'produced': (0.00, 0.20, 1.00),
            'consumed': (1.00, 0.18, 0.00),
            'exported': (0.00, 1.00, 0.25)
            }
        self.mod_depth = 0.45
        self.mod_period = float(pixel_count) / ( 4.0 * math.pi )
        self.produced_power = 0.0
        self.consumed_power = 0.0
        self.current_range = 0
        self.current_speed = 0.0
        self.current_phase = 0.0
        self.current_time = float(time.time())
        if self.iq_envoy is not None:
            self.iq_envoy.data_callbacks.append(self.new_data)

    def new_data(self, data):
        self.produced_power = data['watts_producing']
        self.consumed_power = data['watts_consuming']
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
        return int(255*pixel[0]), int(255*pixel[1]), int(255*pixel[2]), int(255*pixel[3])

    def add_pixels_importing(self, arr):
        self.update_time_phase()
        for i in range(self.pixel_count):
            if self.power_at_index(i) < self.produced_power:
                arr[i] = self.fixed_color('produced')+(0,)
            else:
                arr[i] = self.modulated_color(i, 'consumed')+(0,)
        return arr

    def add_pixels_exporting(self, arr):
        self.update_time_phase()
        for i in range(self.pixel_count):
            if self.power_at_index(i) < self.consumed_power:
                arr[i] = self.fixed_color('produced')+(0,)
            else:
                arr[i] = self.modulated_color(i, 'exported', True)+(0,)
        return arr

    def update_time_phase(self):
        t = float(time.time())
        dt = t - self.current_time
        self.current_time = t
        self.current_phase = self.current_phase + 2*math.pi*dt*self.current_speed

    def modulated_color(self, pixel_id, type=None, reverse=False):
        theta = float(pixel_id) / self.mod_period
        phi = self.current_phase
        phi = -1.0*phi*reverse + phi*1.0*( not reverse)
        amp = math.sin(phi + theta)
        amp = 1 - self.mod_depth + self.mod_depth * amp
        return self.fixed_color(type, amp)

    def fixed_color(self, type=None, amp=1.0):
        return self.hsv_color(
            color=self.colors.get(type, self.bg_color),
            sat=0.95,
            amp=amp
        )
    def set_current_speed(self):
        self.current_speed = round(self.total_power/10000,2)

    def index_at_power(self, pwr):
        if pwr > self.total_power:
            return self.pixel_count - 1
        return int(self.pixel_count * float(pwr) / self.total_power )

    def power_at_index(self, i):
        return self.total_power * float(i)/float(self.pixel_count)

    @property
    def total_power(self):
        return max(self.produced_power, self.consumed_power)

    def hsv_color(self, color=(1.0, 1.0, 1.0), amp=1.0, sat=1.0):
        hsvc = colorsys.rgb_to_hsv(*color)
        hsvc = (hsvc[0], hsvc[1]*sat, hsvc[2]*amp)
        return colorsys.hsv_to_rgb(*hsvc)



if __name__ == '__main__':
    cm = ImportExportMeter()
    cm.consumed_power = 2000.0
    cm.set_current_speed()
    for j in range(100):
        print(cm.pixels)
        time.sleep(0.1)
