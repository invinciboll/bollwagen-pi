# Interface to send dmx values to OLA-Server running locally
import requests


def set(ch_1, ch_2, ch_3, ch_4):
    pload = {'u': '1', 'd': f'{ch_1},{ch_2},{ch_3},{ch_4}'}
    r = requests.post('http://localhost:9090/set_dmx', data=pload)
    print(f"OLA-response: {r.text}")
