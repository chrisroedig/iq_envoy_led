import math
import random
import time

class ProductionMeter():
    def __init__(self, iq_envoy=None, pixel_count=32, max_power = 1500):
        self.iq_envoy = iq_envoy
        self.pixel_count = pixel_count
        self.idle_color = (0, 2, 5)
        self.active_color = (0, 60, 20)
        self.max_power = max_power
        self.pos_factor = float(self.pixel_count) / float(self.max_power)
        self.mod_speed = 5.0
        if self.iq_envoy is not None:
            self.get_power = self.get_iq_envoy_inverter_power
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

    def get_iq_envoy_inverter_power(self):
        return self.iq_envoy.inverter_power

    def get_power(self):
        return random.random()*500+1000

    def modulated_color(self, i):
        return (
                int(self.active_color[0] * self.color_amp(i)),
                int(self.active_color[1] * self.color_amp(i)),
                int(self.active_color[2] * self.color_amp(i)))
    def color_amp(self, pos):
        t = float(time.time())
        amp = math.sin(t*self.mod_speed+pos)
        return (1 + (-.4 - amp*0.4)) * (.5 + .5 * float(pos) / self.pos)


if __name__ == '__main__':
    cm = ProductionMeter()
    print cm.pixels
