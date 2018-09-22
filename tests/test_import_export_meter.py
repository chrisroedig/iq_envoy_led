from .. import import_export_meter

class MeterTest():
    def __init__(self):
        self.consumed_power = 0
        self.produced_power = 0
        self.meter = import_export_meter.ImportExportMeter()
        self.meter.get_consumed_power  = self.get_consumed_power
        self.meter.get_produced_power  = self.get_produced_power
    def get_consumed_power(self):
        return self.consumed_power
    def get_produced_power(self):
        return self.produced_power

def test_power_range_ramp():
    mt = MeterTest()
    for p in range(100):
        mt.consumed_power = float(p*100)
        assert(isinstance(mt.meter.current_range,int))

def test_gridlines_ramp():
    mt = MeterTest()
    for p in range(100):
        mt.consumed_power = float(p*100)
        arr = [mt.meter.bg_color]*mt.meter.pixel_count
        assert(isinstance(mt.meter.mod_gridline_pixels(arr),list))
