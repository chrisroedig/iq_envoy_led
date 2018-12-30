import math
import random
import time

class Uniform():
    def __init__(self, **kwargs):
        self.pixel_count = kwargs.get('pixel_count', 32)
        self.colors = kwargs.get('colors', [(0,0,0,0), (255,255,255,255)])
        self.gradient_steps = kwargs.get('gradient_steps', 100)
        self.color_cache = None
        self.current_mix = 0.0
        self.build_color_cache()

    def __getitem__(self, key):
        if type(key) == int:
            key = slice(key, None)
        return self.pixels(key.start, key.stop)

    def pixels(self, start, stop=None):
        if stop is None:
            return self.fixed_color
        return [self.fixed_color(self.current_mix)] * (stop-start)

    def fixed_color(self, mix):
        return self.color_cache[min(int(round(mix*self.gradient_steps)),self.gradient_steps-1)]

    def calc_gradient_color(self, gradient_pos):
        n = len(self.colors)
        a_color = self.colors[max(0,int(math.floor(n*gradient_pos))-1)]
        b_color = self.colors[min((n-1),int(math.ceil(n*gradient_pos))-1)]
        mix = n*gradient_pos - math.floor(n*gradient_pos)
        return tuple(self.calc_mixed_color(a_color, b_color, mix))

    def calc_mixed_color(self, a_color, b_color, mix):
        color = [0] * len(a_color)
        for i, c in enumerate(color):
            color[i] = a_color[i] * (1.0-mix) + b_color[i] * mix
        return color

    def build_color_cache(self):
        ccache = []
        for i in range(self.gradient_steps):
            m = i / float(self.gradient_steps)
            ccache.append(self.calc_gradient_color(m))
        self.color_cache = tuple(ccache)

class Wave(Uniform):
    def __init__(self, **kwargs):
        Uniform.__init__(self,**kwargs)
        self.speed = kwargs.get('speed', 1.0)
        self.period = kwargs.get('period', None)
        if self.period is None:
            self.period = float(self.pixel_count) / ( 4.0 * math.pi )
        self.reverse = kwargs.get('reverse', False)

        self.phase = 0.0
        self.time = float(time.time())
        self.mod_depth = 1.0

    def pixels(self, start, stop=None):
        if stop is None:
            self.modulated_color(start)
        return [self.modulated_color(i) for i in range(start, stop)]

    def update_time_phase(self):
        t = float(time.time())
        dt = t - self.time
        self.time = t
        self.phase = self.phase + 2*math.pi*dt*self.speed

    def modulated_color(self, pixel_id):
        theta = float(pixel_id) / self.period
        phi = self.phase
        phi = -1.0 * phi * self.reverse + phi * 1.0 * ( not self.reverse )
        amp = math.sin(phi + theta)
        amp = self.mod_depth * amp
        c = self.fixed_color(amp)
        return c

class Pulse(Uniform):
    def __init__(self, **kwargs):
        pass

class Sparks(Uniform):
    def __init__(self, **kwargs):
        pass

if __name__ == '__main__':
    colors = [
        (255, 0, 0, 0),
        (0, 0, 255, 0)
        ]
    upixels = Wave(pixel_count=32, colors=colors)
    print(upixels[3:38])
