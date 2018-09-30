import requests
from threading import Timer

class IQEnvoy():
    def __init__(self, **kwargs):
        self.host = kwargs.get('host','envoy.local')
        self.home_data = None
        self.production_data = None
        self.inventory_data = None
        self.polling_active = False
        self.poll_timer = None

    def get_data(self):
        self.production_data = self.get_production_data()
        self.on_new_data({
            'watts_producing': self.inverter_power, 
            'watts_consuming': self.consumption_power
            })
    def on_new_data(self, data):
        # override with callback
        pass
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
