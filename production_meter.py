import math
import random

class ProductionMeter():
    def __init__(self, iq_envoy=None, pixel_count=32, max_power=5000):
        self.iq_envoy = iq_envoy
        self.active_color = [20, 115,50]
        self.idle_color = [0, 0,50]
        self.pixel_count = pixel_count
        self.max_power = max_power
        self.pos_factor = float(self.pixel_count) / float(self.max_power)
        if self.iq_envoy is not None:
            self.power = self.iq_envoy.inverter_power
    @property
    def pixels(self):
        arr = [ self.idle_color ] * self.pixel_count
        for i in range(0 , int(math.floor(self.power * self.pos_factor))):
            arr[i] = self.active_color
        return arr
    @property
    def power(self):
        return random.random() * self.max_power
