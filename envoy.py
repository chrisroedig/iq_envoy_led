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
        self.home_data = self.get_home_data()
        self.production_data = self.get_production_data()
        self.inventory_data = self.get_inventory_data()

    def get_home_data(self):
        return self.json_request('home')

    def get_production_data(self):
        return self.json_request('production')

    def get_inventory_data(self):
        return self.json_request('inventory')

    def json_request(self, file):
        return requests.get('http://'+self.host+'/'+file+'.json').json()

    @property
    def inverter_production(self):
        if self.production_data is None:
            return None
        return next(p for p in self.production_data['production'] if p['type'] == 'inverters')

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
        print 'getting data...'
        self.get_data()
        print 'wattage: '+str(self.inverter_power)
        self.poll_timer = Timer(10.0, self.poll_for_data).start()

    def stop_polling(self):
        self.polling_active = False
        self.poll_timer = None
