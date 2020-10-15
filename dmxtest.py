from DmxPy import DmxPy
import time

dmx = DmxPy('/dev/ttyUSB0')
i = 0
for _ in range(512):
    dmx.setChannel(i, 100)

dmx.render()
