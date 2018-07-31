# IQEnvoy LED

## Idea

The enphase IQEnvoy device is designed to monitor microinverter output for a solar panel array. It reports the data to the cloud, but also exposes a local web interface.
Using the underlying json files you can query the current production, consumption and individual inverter data easily:

- Basic Status Info: http://envoy.local/home.json
- Energy production, sonsumption and storage info: http://envoy.local/production.json
- Data from monitored equipment: http://envoy.local/invenotry.json

The repo is some code designed to run on a raspberry PI with an attached neopixel strip (and other indicators), to visualize the current state of the system.

## Features (coming soon)

- Overall production meter
- Production vs. Consumption balance meter
- Panel by Panel performance on LED strip
- Integrate DAC circuit to drive an actual physical gauge 


