import math
import random
import time

class ConsumptionMeter():
    def __init__(self, iq_envoy=None, pixel_count=32, max_power=8000):
        self.iq_envoy = iq_envoy
        self.active_color = (200, 20,00)
        self.idle_color = (10, 0,0)
        self.pixel_count = pixel_count
        self.max_power = max_power
        self.pos_factor = float(self.pixel_count) / float(self.max_power)
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
    
    def get_iq_envoy_consumption_power(self):
        return self.iq_envoy.consumption_power
    
    def get_power(self):
        return random.random()*500+4000

    def modulated_color(self, i):
        return (    
                int(self.active_color[0] * self.wave_amp(i)),
                int(self.active_color[1] * self.wave_amp(i)),
                int(self.active_color[2] * self.wave_amp(i)))
    def wave_amp(self, pos):
        t = float(time.time())
        amp = math.sin(-t*5.0+pos)
        return 1.0 -.3 - amp*0.3
