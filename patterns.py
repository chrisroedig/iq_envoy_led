import math
import random
import time

class Uniform():
    def __init__(self, **kwargs):
        self.pixel_count = kwargs['pixel_count']
        self.colors = kwargs['colors']
        self.gradient_steps = kwargs.get('gradient_steps', 100)
    def fixed_color(self):
        pass
    def gradient_color(self, gradient_pos):
        n = len(self.colors)
        a_color = self.colors[max(0,int(math.floor(n*gradient_pos)))]
        b_color = self.colors[min((n-1),int(math.ceil(n*gradient_pos)))]
        mix = n*gradient_pos - math.floor(n*gradient_pos)
        return tuple(self.mixed_color(a_color, b_color, mix))
    def mixed_color(self, a_color, b_color, mix):
        color = [0] * len(a_color)
        for i, c in enumerate(color):
            color[i] = a_color[i] * (1.0-mix) + b_color[i] * mix
        return color
    def build_color_cache(self):


class Wave(Uniform):
    def __init__(self, **kwargs):
        self.speed = kwargs['speed']
        self.period = kwargs['period']
        self.phase = 0.0
        self.time = float(time.time())


class Pulse(Uniform):
    def __init__(self, **kwargs):
        pass

class Sparks(Uniform):
    def __init__(self, **kwargs):
        pass

if __name__ == '__main__':
    colors = [
        (255, 0, 0, 0),
        (255, 255, 255, 255),
        (0, 0, 255, 0),
        (0, 0, 0, 255)
        ]
    upixels = Uniform(pixel_count=32, colors=colors)
    for i in range(20):
        m = i/20.0
        print(upixels.gradient_color(m))
