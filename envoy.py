import requests
from threading import Timer
import time
import sys
import signal

class IQEnvoy():
    def __init__(self, **kwargs):
        self.host = kwargs.get('host','envoy.local')
        self.home_data = None
        self.production_data = None
        self.inventory_data = None
        self.polling_active = False
        self.poll_timer = None
        self.data_callbacks = []

    def get_data(self):
        try:
            self.production_data = self.get_production_data()
        except Exception as ex:
            print('failed to get data')
            print(ex)
            return
        self.on_new_data({
            'watts_producing': self.inverter_power,
            'watts_consuming': self.consumption_power,
            'watts_avg_7d_consumption': self.avg_7d_consumption,
            'watts_avg_7d_production': self.avg_7d_production,
            'wh_today_consumed' : self.today_consumption,
            'wh_today_produced' : self.today_production
            })
    def on_new_data(self, data):
        for fn in data_callbacks:
            fn(data)
    def get_home_data(self):
        return self.json_request('home')

    def get_production_data(self):
        return self.json_request('production')

    def get_inventory_data(self):
        return self.json_request('inventory')

    def json_request(self, f):
        resp =  requests.get('http://'+self.host+'/'+f+'.json')
        return resp.json()


    @property
    def inverter_production(self):
        if self.production_data is None:
            return None
        return next(p for p in self.production_data['production'] if p.get('measurementType') == 'production')

    @property
    def total_consumption(self):
        if self.production_data is None:
            return None
        return next(p for p in self.production_data['consumption'] if p.get('measurementType') == 'total-consumption')

    @property
    def consumption_power(self):
        if self.total_consumption is None:
            return 0.0
        return abs(self.total_consumption['wNow'])

    @property
    def inverter_power(self):
        if self.inverter_production is None:
            return 0.0
        return self.inverter_production['wNow']

    @property
    def avg_7d_consumption(self):
        if self.total_consumption is None:
            return 0.0
        return self.total_consumption['whLastSevenDays'] / (7*24)

    @property
    def avg_7d_production(self):
        if self.inverter_production is None:
            return 0.0
        return self.inverter_production['whLastSevenDays'] / (7*24)

    @property
    def today_consumption(self):
        if self.total_consumption is None:
            return 0.0
        return self.total_consumption['whToday']

    @property
    def today_production(self):
        if self.inverter_production is None:
            return 0.0
        return self.inverter_production['whToday']



    def start_polling(self):
        if self.polling_active == True:
            return
        self.polling_active = True
        self.poll_for_data()

    def poll_for_data(self):
        if self.polling_active != True:
            return
        self.get_data()
        self.poll_timer = Timer(2.0, self.poll_for_data).start()

    def stop_polling(self):
        self.polling_active = False
        self.poll_timer = None


if __name__ == '__main__':
    def new_data_handler(data):
        print('got new data')
        print(data)
    e = IQEnvoy()
    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        e.stop_polling()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    e.on_new_data = new_data_handler
    e.start_polling()
    while True:
        time.sleep(.25)
