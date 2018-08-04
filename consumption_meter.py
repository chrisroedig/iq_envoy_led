import math
import random
import time

class ConsumptionMeter():
    def __init__(self, iq_envoy=None, pixel_count=32, max_lo=2000 ,max_hi=8000):
        self.iq_envoy = iq_envoy
        self.pixel_count = pixel_count
        self.idle_color_lo = (15, 11,0)
        self.idle_color_hi = (24, 1, 0)
        self.active_color_lo = (110, 70,00)
        self.active_color_hi = (240, 10,00)
        self.max_power_hi = max_hi
        self.max_power_lo = max_lo
        if self.iq_envoy is not None:
            self.get_power = self.get_iq_envoy_consumption_power
    @property
    def pixels(self):
        arr = [ self.idle_color ] * self.pixel_count
        for i in range(0 , self.pos):
            arr[i] = self.modulated_color(i)
        return arr

    @property
    def pos(self):
        pixel = int( self.pos_factor * self.get_power() )
        return min(self.pixel_count-1, pixel)

    @property
    def active_color(self):
        if self.get_power() < self.max_power_lo:
            return self.active_color_lo
        else:
            return self.active_color_hi
    @property
    def idle_color(self):
        if self.get_power() < self.max_power_lo:
            return self.idle_color_lo
        else:
            return self.idle_color_hi

    @property
    def pos_factor(self):
        if self.get_power() < self.max_power_lo:
            return float(self.pixel_count) / float(self.max_power_lo)
        else:
            return float(self.pixel_count) / float(self.max_power_hi)
    @property
    def mod_speed(self):
        if self.get_power() < self.max_power_lo:
            return 2.0
        else:
            return 5.0

    def get_iq_envoy_consumption_power(self):
        return self.iq_envoy.consumption_power

    def get_power(self):
        return random.random()*500+1000

    def modulated_color(self, i):
        return (
                int(self.active_color[0] * self.color_amp(i)),
                int(self.active_color[1] * self.color_amp(i)),
                int(self.active_color[2] * self.color_amp(i)))
    def color_amp(self, pos):
        t = float(time.time())
        amp = math.sin(-t*self.mod_speed+pos)
        return (1 + (-.4 - amp*0.4)) * (.5 + .5 * float(pos) / self.pos)


if __name__ == '__main__':
    cm = ConsumptionMeter()
    print cm.pixels
